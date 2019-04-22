from excel_util import WebExcelSchedule, WebExcelMetrics, WebExcelHelper

if __name__ == '__main__':
    sched = WebExcelSchedule()
    sched.read_file('data_files/Machine Schedule 1-29-2019.xlsx', sheet_name = 'MC12', header = 1)
    sched.read_schedule()
    sched.sanity_check()
    sched.gen_id('work_order', 'set_number')
    sched1 = WebExcelSchedule()
    sched1.read_file('data_files/Machine Schedule 1-29-2019.xlsx', sheet_name = 'MC28', header = 1)
    sched1.read_schedule()
    sched1.sanity_check()
    sched1.gen_id('work_order', 'set_number')

    metric = WebExcelMetrics()
    metric.read_file('data_files/New Plant Metrics rev 1-1-2019.xlsx', sheet_name = 'Data', header = 0)
    metric.parse_metrics()
    metric.filters()
    metric.gen_id('OpWorkOrderID', 'SetNum')

    df1 = sched.datadf.append(sched1.datadf)
    df2 = metric.datadf

    s2m = WebExcelHelper.merge_schedule_metrics(df1, df2)
    m2s = WebExcelHelper.merge_schedule_metrics(df2, df1)

    s2m.to_csv('Schedule-Metrics.csv', index = False)
    m2s.to_csv('Metrics-Schedule.csv', index = False)
    sched.write_data("MC12.csv")
    sched1.write_data("MC28.csv")
    metric.write_data("Metrics.csv")
