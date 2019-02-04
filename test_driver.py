from excel_util import WebExcelSchedule

if __name__ == '__main__':
    web = WebExcelSchedule()
    web.read_file('data_files/Machine Schedule 1-29-2019.xlsx', sheet_name = 'MC12', header = 1)
    web.read_schedule()
    web.sanity_check()
    # print(web.datadf)
    # print(web.merge_workorder())
    web.write_data()
