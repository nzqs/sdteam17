import collections
import pandas as pd
from ortools.sat.python import cp_model

def read_dummy_data(data_file = "dummy_schedule_input.xlsx"):
    df = pd.read_excel(data_file)
    data = []
    # For each job, let thawing be task 0, processing be task 1
    # Each task = (task id, time); Job = [ordered tasks]
    for index, work_set in df.iterrows():
        job = [(0, work_set['thaw_time']), (1, work_set['processing_time'])]
        data.append(job)
    return data

def read_dummy_data2(data_file = "dummy_schedule_input.xlsx"):
    df = pd.read_excel(data_file)
    df = df.astype(int, errors = 'ignore')
    data = {}
    # For each job, let thawing be task 0, processing be task 1
    # Each task = (task id, time); Job = [ordered tasks]
    for index, work_set in df.iterrows():
        job = [(0, int(work_set['thaw_time'])), (1, int(work_set['processing_time']))]
        data[(work_set['work_order'], work_set['set_id'], work_set['material'])] = job
    return data

def MinimalJobshopSat():
    """Minimal jobshop problem."""
    # Create the model.
    model = cp_model.CpModel()

    M = 50000

    jobs_full = read_dummy_data2()
    jobs_data = list(jobs_full.values()) # List of lists
    jobs_ids = list(jobs_full.keys())

    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)
    jobs_count = len(jobs_full)
    jobs_count_range = range(jobs_count)

    # Compute horizon.
    horizon = sum(task[1] for job in jobs_data for task in job)

    task_type = collections.namedtuple('task_type', 'start end interval setup parameters')
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index setup parameters')

    # Create jobs.
    all_tasks = {}
    for job, work_id in enumerate(jobs_full):
        for task_id, job_data in enumerate(jobs_full[work_id]):
            start_var = model.NewIntVar(0, horizon,
                                        'start_%i_%i' % (job, task_id))
            duration = job_data[1]
            end_var = model.NewIntVar(0, horizon, 'end_%i_%i' % (job, task_id))
            interval_var = model.NewIntervalVar(
                start_var, duration, end_var, 'interval_%i_%i' % (job, task_id))
            setup_req = model.NewBoolVar('setup_%i_%i' % (job, task_id))
            all_tasks[job, task_id] = task_type(
                start=start_var, end=end_var, interval=interval_var, setup = setup_req, parameters = work_id)

    # Create and add disjunctive constraints. Only one job running on this machine
    for machine in all_machines:
        intervals = []
        for job in jobs_count_range:
            for task_id, task in enumerate(jobs_data[job]):
                if (task[0] == machine) and (machine == 1):
                    # Second clause ensures only slitting needs to be disjunctive
                    intervals.append(all_tasks[job, task_id].interval)
        model.AddNoOverlap(intervals)

    # Add precedence contraints.
    # Thawing must occur before slitting.
    for job in jobs_count_range:
        for task_id in range(0, len(jobs_data[job]) - 1):
            model.Add(all_tasks[job, task_id +
                                1].start >= all_tasks[job, task_id].end)

    # 36 hour thaw, 72 hour max out time
    for job in jobs_count_range:
        task_id = 0
        # Pick thaw jobs, then ensure the ending of next job (slitting)
        # and the start of the thaw job are 72 hours apart
        model.Add(all_tasks[job, task_id + 1].end - all_tasks[job, task_id].start <= 72)
        # Ensure at least 36 hours thaw
        model.Add(all_tasks[job, task_id].end - all_tasks[job, task_id].start >= 36)

    # Si = 1 if setup required. Only slitting requires jobs to be grouped
    # This is incorrect logic. It will check the previous job and assign a setup
    # if the previous job has a different material.
    # However the previous job is already set. IOW this constraint checks the
    # generated schedule and assigns setups accordingly.
    # Instead, this constraint must be a graph theory approach (arc constraints)
    # Map the transitions of each job then assign each transition a weight (if the
    # transition involves setup, weight = 5, else weight = 0) and penalize the weights
    # Then, the arc constraint seeks a path through all the tasks that minimizes weight penalty.
    # sounds like alot of work omg.
    for job in range(1, jobs_count):
        for task_id in range(0, len(jobs_data[job])):
            if task_id == 1:
                model.Add(int(all_tasks[job, task_id].parameters[1]) - int(all_tasks[job - 1, task_id].parameters[1]) <= M * all_tasks[job, task_id].setup)
                model.Add(-int(all_tasks[job, task_id].parameters[1]) + int(all_tasks[job - 1, task_id].parameters[1]) <= M * all_tasks[job, task_id].setup)

    # Calculate setup
    def calc_setup():
        setups = []
        parameters = list(jobs_full.keys())
        # List comprehension for initial set up. Assumed none
        setups.append([0 for _ in range(len(jobs_full))])
        for i, source in enumerate(parameters):
            setup_time = []
            for j, destination in enumerate(parameters):
                # Same WO, therefore same material
                if destination[0] == source[0]:
                    setup_time.append(0)
                # Same material
                elif (destination[1] == source[1]):
                    setup_time.append(1)
                # Different WO and material
                else:
                    setup_time.append(5)
            setups.append(setup_time)
        return setups
    setups = calc_setup()
    # Circuit constraint
    arcs = []
    for i in jobs_count_range:
        for j in jobs_count_range:
            if i == j:
                continue
            literal = model.NewBoolVar('%i follows %i' % (j, i))
            arcs.append([i + 1, j + 1, literal])

            # Link the times to tasks
            model.Add(all_tasks[(j, 1)].start >= all_tasks[(i, 1)].end + setups[i + 1][j]).OnlyEnforceIf(literal)
    model.AddCircuit(arcs)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(
        obj_var,
        [all_tasks[(job, len(jobs_data[job]) - 1)].end for job in jobs_count_range])
    model.Minimize(obj_var)

    # Downtime objective.
    # obj_var = model.NewIntVar(0, horizon, 'downtime')
    # model.AddMaxEquality(
    #     obj_var,
    #     [all_tasks[job, len(jobs_data[job]) - 1].start - all_tasks[job, len(jobs_data[job]) - 2].end for job in range(1, jobs_count -1)])
    # model.Minimize(obj_var)

    # Setup objective.
    # obj_var = model.NewIntVar(0, len(jobs_data), 'setups')
    # model.AddMaxEquality(
    #     obj_var,
    #       [all_tasks[(job, len(jobs_data[job]) - 1)].setup for job in jobs_count_range])
    # model.Minimize(sum([all_tasks[(job, 1)].setup for job in jobs_count_range]))

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # Print out makespan.
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        print()

        # Create one list of assigned tasks per machine.
        assigned_jobs = [[] for _ in all_machines]
        for job in jobs_count_range:
            for task_id, task in enumerate(jobs_data[job]):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(
                        start=solver.Value(all_tasks[job, task_id].start),
                        job=job,
                        index=task_id,
                        setup = solver.Value(all_tasks[job, task_id].setup),
                        parameters = all_tasks[job, task_id].parameters))

        disp_col_width = 10
        sol_line = ''
        sol_line_tasks = ''

        print('Optimal Schedule', '\n')

        for machine in all_machines:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line += 'Process ' + str(machine) + ': '
            sol_line_tasks += 'Process ' + str(machine) + ': '

            for assigned_task in assigned_jobs[machine]:
                name = 'job_%i_%i' % (assigned_task.job, assigned_task.index)
                # Add spaces to output to align columns.
                sol_line_tasks += name + ' ' * (disp_col_width - len(name))
                start = assigned_task.start
                duration = jobs_data[assigned_task.job][assigned_task.index][1]
                setup = assigned_task.setup

                sol_tmp = '[%i,%i,%i]' % (start, start + duration, setup)
                # Add spaces to output to align columns.
                sol_line += sol_tmp + ' ' * (disp_col_width - len(sol_tmp))

            sol_line += '\n'
            sol_line_tasks += '\n'

        print(sol_line_tasks)
        print('Task Time Intervals\n')
        print(sol_line)


    # QUICK AND DIRTY HACK TO WRITE SCHEDULE TO CSV
    # Also report pull finish, and also compute the interval between all starts and finishes
    # df = pd.DataFrame(columns = ['job_id', 'pull', 'slitting_start', 'slitting_finish'])
    # pull = [job.start for job in assigned_jobs[0]]
    # slitting_start = [job.start for job in assigned_jobs[1]]
    # slitting_finish = [job.start + jobs_data[job.job][job.index][1] for job in assigned_jobs[1]]
    # job_id = [job.parameters[:2] for job in assigned_jobs[1]]
    # columns = [job_id, pull, slitting_start, slitting_finish]
    # for i, col in enumerate(df.columns):
    #     df[col] = columns[i]
    # df.to_csv('dummy_schedule.csv', index = False)

if __name__ == '__main__':
    MinimalJobshopSat()
