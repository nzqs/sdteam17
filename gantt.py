import plotly.plotly as py
import plotly.offline as offline
import plotly.figure_factory as ff
import pandas as pd

from excel_util import WebExcelSchedule

if __name__ == '__main__':
    web = WebExcelSchedule()
    web.read_file('data_files/Machine Schedule 1-29-2019.xlsx', sheet_name = 'MC28', header = 1)
    web.read_schedule()
    web.sanity_check()
    df = web.merge_workorder()
    df = df.rename(index=str, columns={'work_order':'Task', 'start_time':'Start', 'end_time':'Finish'})
    fig = ff.create_gantt(df, showgrid_x=True, showgrid_y=True)
    offline.plot(fig, auto_open = True, filename = 'Web Scheduling Gantt.html')
