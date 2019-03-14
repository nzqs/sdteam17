# Copyright 2010-2018 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Single machine jobshop with setup times, release dates and due dates."""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import argparse
import pandas as pd

from ortools.sat.python import cp_model
from google.protobuf import text_format

#----------------------------------------------------------------------------
# Command line arguments.
PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    '--output_proto',
    default='',
    help='Output file to write the cp_model'
    'proto to.')
PARSER.add_argument('--params', default='', help='Sat solver parameters.')
PARSER.add_argument(
    '--preprocess_times',
    default=True,
    type=bool,
    help='Preprocess setup times and durations')


#----------------------------------------------------------------------------
# Intermediate solution printer
class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def on_solution_callback(self):
        print('Solution %i, time = %f s, objective = %i' %
              (self.__solution_count, self.WallTime(), self.ObjectiveValue()))
        self.__solution_count += 1


def main(args):
    """Solves a complex single machine jobshop scheduling problem."""

    parameters = args.params
    output_proto = args.output_proto

    #----------------------------------------------------------------------------
    # Data.

    df = pd.read_excel('dummy_schedule_input.xlsx')

    job_durations = list(df['processing_time'])

    # Populate a matrix mapping the setup transitions from job to job.
    # Initial setup = 0 for now. Possibly pass in current state and calculate later
    def calc_setup(df = df):
        setups = []
        parameters = [(df['work_order'][i], df['set_id'][i]) for i in range(len(df))]
        # List comprehension for initial set up. Assumed none
        setups.append([0 for _ in range(len(df))])
        for i, source in enumerate(parameters):
            setup_time = []
            for j, destination in enumerate(parameters):
                # if i == j:
                #     continue
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
    setup_times = calc_setup()

    due_dates = list(df['due_by'])

    release_dates = [0 for i in range(len(df))]

    precedences = [(0, 2), (1, 2)]

    #----------------------------------------------------------------------------
    # Helper data.
    num_jobs = len(job_durations)
    all_jobs = range(num_jobs)

    #----------------------------------------------------------------------------
    # Preprocess.
    if args.preprocess_times:
        for job_id in all_jobs:
            min_incoming_setup = min(
                setup_times[j][job_id] for j in range(num_jobs + 1))
            if release_dates[job_id] != 0:
                min_incoming_setup = min(min_incoming_setup,
                                         release_dates[job_id])
            if min_incoming_setup == 0:
                continue

            print('job %i has a min incoming setup of %i' %
                  (job_id, min_incoming_setup))
            # We can transfer some setup times to the duration of the job.
            job_durations[job_id] += min_incoming_setup
            # Decrease corresponding incoming setup times.
            for j in range(num_jobs + 1):
                setup_times[j][job_id] -= min_incoming_setup
            # Adjust release dates if needed.
            if release_dates[job_id] != 0:
                release_dates[job_id] -= min_incoming_setup

    #----------------------------------------------------------------------------
    # Model.
    model = cp_model.CpModel()

    #----------------------------------------------------------------------------
    # Compute a maximum makespan greedily.
    horizon = sum(job_durations) + sum(
        max(setup_times[i][j] for i in range(num_jobs + 1))
        for j in range(num_jobs))
    print('Greedy horizon =', horizon)

    #----------------------------------------------------------------------------
    # Global storage of variables.
    intervals = []
    starts = []
    ends = []

    #----------------------------------------------------------------------------
    # Scan the jobs and create the relevant variables and intervals.
    for job_id in all_jobs:
        duration = job_durations[job_id]
        release_date = release_dates[job_id]
        due_date = due_dates[job_id] if due_dates[job_id] != -1 else horizon
        print('job %2i: start = %5i, duration = %4i, end = %6i' %
              (job_id, release_date, duration, due_date))
        name_suffix = '_%i' % job_id
        start = model.NewIntVar(release_date, due_date, 's' + name_suffix)
        end = model.NewIntVar(release_date, due_date, 'e' + name_suffix)
        interval = model.NewIntervalVar(start, duration, end,
                                        'i' + name_suffix)
        starts.append(start)
        ends.append(end)
        intervals.append(interval)

    # No overlap constraint.
    model.AddNoOverlap(intervals)

    #----------------------------------------------------------------------------
    # Out time.
    for job in all_jobs:
        model.Add(ends[job] - starts[job] <= 36)

    #----------------------------------------------------------------------------
    # Transition times using a circuit constraint.
    arcs = []
    for i in all_jobs:
        # Initial arc from the dummy node (0) to a task.
        start_lit = model.NewBoolVar('')
        arcs.append([0, i + 1, start_lit])
        # If this task is the first, set to minimum starting time.
        min_start_time = max(release_dates[i], setup_times[0][i])
        model.Add(starts[i] == min_start_time).OnlyEnforceIf(start_lit)
        # Final arc from an arc to the dummy node.
        arcs.append([i + 1, 0, model.NewBoolVar('')])

        for j in all_jobs:
            if i == j:
                continue

            lit = model.NewBoolVar('%i follows %i' % (j, i))
            arcs.append([i + 1, j + 1, lit])

            # We add the reified precedence to link the literal with the times of the
            # two tasks.
            # If release_dates[j] == 0, we can strenghten this precedence into an
            # equality as we are minimizing the makespan.
            if release_dates[j] == 0:
                model.Add(starts[j] == ends[i] +
                          setup_times[i + 1][j]).OnlyEnforceIf(lit)
            else:
                model.Add(starts[j] >= ends[i] +
                          setup_times[i + 1][j]).OnlyEnforceIf(lit)

    model.AddCircuit(arcs)

    #----------------------------------------------------------------------------
    # Precedences. Unused for now
    for before, after in precedences:
        # print('job %i is after job %i' % (after, before))
        # model.Add(ends[before] <= starts[after])
        pass

    #----------------------------------------------------------------------------
    # Objective.
    makespan = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(makespan, ends)
    model.Minimize(makespan)


    #----------------------------------------------------------------------------
    # Write problem to file.
    if output_proto:
        print('Writing proto to %s' % output_proto)
        with open(output_proto, 'w') as text_file:
            text_file.write(str(model))

    #----------------------------------------------------------------------------
    # Solve.
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30
    if parameters:
        text_format.Merge(parameters, solver.parameters)
    solution_printer = SolutionPrinter()
    solver.SolveWithSolutionCallback(model, solution_printer)
    print(solver.ResponseStats())
    for job_id in all_jobs:
        print(
            'job %i starts at %i end ends at %i' %
            (job_id, solver.Value(starts[job_id]), solver.Value(ends[job_id])))


if __name__ == '__main__':
    main(PARSER.parse_args())
