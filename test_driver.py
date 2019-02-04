from excel_util import WebExcel

if __name__ == '__main__':
    web = WebExcel()
    web.read_file('data_files/Machine Schedule 1-29-2019.xlsx', sheet_name = 'MC28', header = 1)
    web.read_schedule()
    web.sanity_check()
    print(web.datadf)
