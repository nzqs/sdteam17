import plotly.plotly as py
import plotly.offline as offline
import plotly.figure_factory as ff
import pandas as pd
<<<<<<< HEAD
import logging

from excel_util import WebExcelSchedule

def main():
    logging.basicConfig(filename = 'gantt.log', level = logging.INFO)
    logging.info('Started creating Gantt chart.')
=======

from excel_util import WebExcelSchedule

if __name__ == '__main__':
>>>>>>> master
    web = WebExcelSchedule()
    web.read_file('data_files/Machine Schedule 1-29-2019.xlsx', sheet_name = 'MC28', header = 1)
    web.read_schedule()
    web.sanity_check()
    df = web.merge_workorder()
    df = df.rename(index=str, columns={'work_order':'Task', 'start_time':'Start', 'end_time':'Finish'})
<<<<<<< HEAD
    colors = dict(Job = (0.2, 0.7, 0.3), Downtime = 'rgb(220, 0, 0)')
    fig = ff.create_gantt(df, showgrid_x=True, showgrid_y=True, colors = colors, index_col = 'Resource', title = 'MC28 Gantt - Work Orders & Downtime')
    offline.plot(fig, auto_open = True, filename = 'Web Scheduling Gantt.html')
    logging.info('Finished creating Gantt chart.')

if __name__ == '__main__':
    main()
=======
    fig = ff.create_gantt(df, showgrid_x=True, showgrid_y=True)
    offline.plot(fig, auto_open = True, filename = 'Web Scheduling Gantt.html')
>>>>>>> master
