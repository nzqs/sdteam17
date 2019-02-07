import pandas as pd
import logging # Call logs from drivers

class WebExcel(object):
    """
    WebExcel class for opening, reading, and parsing Web's excel files.
    Class initializes with default objects:
        df: Empty Pandas DataFrame object
        datadict: Dictionary with desired attributes as keys mapped to empty lists
        datadf: DataFrame to hold parsed data
    """
    def __init__(self):
        super(WebExcel, self).__init__()
        self.df = pd.DataFrame()
        self.datadict = {
            # Sample attributes
            # 'processing_time': [],
            # 'thaw_time': []
            }
        self.datadf = pd.DataFrame()

    # Open Excel file and read given sheet. Assume headers on second row.
    def read_file(self, file_name, sheet_name, header = 1):
        self.df = pd.read_excel(file_name, sheet_name = sheet_name, header = header)

    def read_orders(self):
        # Placeholder to read client submitted 90 day schedule
        pass

    def read_tables(self):
        # Placeholder to read table of known values
        # Processing time per material, thaw time per material etc.
        pass

    def write_data(self, out_file = "Web Data.csv"):
        # TODO: Read df, parse necessary values and dump
        # out_file is file name
        # Placeholder implementation. Real values should be in a DataFrame
        self.datadf.to_csv(out_file, index = False)

    def gen_id(self, *args):
        # Combine given *args columns into a new column

class WebExcelSchedule(WebExcel):
    """
    Subclass of WebExcel
    Implement methods to handle Schedule files
    """
    def __init__(self):
        super(WebExcelSchedule, self).__init__()
        self.wodf = pd.DataFrame()

    def read_schedule(self):
        # Parse proposed schedule
        # Implement similar methods for differently formatted files
        # Take schedule file and parse for processing time, thaw time, and more
        # Pass these values into data
        # Psuedocode: data['processing_time'] = self.df.end_time - self.df.start_time

        # Attribute declaration and assignment
        columns = ['work_order','set_number', 'part_number', 'processing_time',
            'start_time', 'end_time', 'thaw_time']
        self.datadf = pd.DataFrame(columns = columns)
        self.datadf.work_order, self.datadf.set_number, self.datadf.start_time, self.datadf.end_time = self.df.WO, self.df.Set, self.df.Start, self.df.Finish
        self.datadf.part_number = self.df.PN
        # Coerce datetime columns to datetime type.
        # Sounds redundant, but this lets us handle empty or invalid data
        self.df.Start = self.df.Start.apply(pd.to_datetime, errors = 'coerce')
        self.df.Finish = pd.to_datetime(arg = self.df.Finish, errors = 'coerce')
        self.df['Pull Material'] = pd.to_datetime(self.df['Pull Material'], errors = 'coerce')
        self.datadf.processing_time = self.df.Finish - self.df.Start
        self.datadf.thaw_time = self.df.Start - self.df['Pull Material']
        # Set work order to downtime
        # May need to backfill some wo
        self.datadf.loc[self.datadf.work_order.isna(), "work_order"] = self.datadf[self.datadf.work_order.isna()].part_number


    def sanity_check(self):
        # Remove crazy values.
        # This implementation is currently only for schedule.
        # Others may be added as needed
        # Processing time can't be negative. Keep positive time deltas
        # self.datadf = self.datadf[self.datadf.processing_time > pd.Timedelta('0 days')]
        self.datadf.drop(self.datadf[self.datadf.processing_time < pd.Timedelta('0 days')].index, inplace = True)

    def merge_workorder(self):
        # TODO: Write seperate class for schedule sheets
        # Merge work orders in the schedule into one row.
        # Must read schedule first, then returns df of merged WO.
        columns = ['work_order', 'start_time', 'end_time']
        wodf = pd.DataFrame(columns = columns)
        downtime_column = ['D - Down', 'D - Setup', 'D- Holiday', 'D- Protocol',
            'D- Shift'] # For some reason, MC12 has D- Shift.
        downtime_column = ['D - Down', 'D - Setup', 'D- Holiday', 'D- Protocol']
        # First, add Downtime blocks, then add WO. Order by start
        down = self.datadf[self.datadf['work_order'].isin(downtime_column)]
        wodf.work_order, wodf.start_time, wodf.end_time = down.work_order, down.start_time, down.end_time
        wo_only = self.datadf[~self.datadf['work_order'].isin(downtime_column)]
        agg = wo_only.groupby('work_order')['start_time', 'end_time'].agg(['first', 'last'])
        agg1 = pd.DataFrame(columns = columns)
        agg1.work_order, agg1.start_time, agg1.end_time = agg.index, list(agg.start_time['first']), list(agg.end_time['last'])
        wodf = wodf.append(agg1)
        del down, wo_only, agg, agg1 # Cleanup
        wodf.start_time = pd.to_datetime(wodf.start_time, errors = 'coerce')
        wodf = wodf.sort_values(by = 'start_time')
        return wodf

class WebExcelMetrics(object):
    """docstring for WebExcelMetrics"""
    def __init__(self):
        super(WebExcelMetrics, self).__init__()
        self.mdf = pd.DataFrame()

    def parse_metrics(self):
        columns = ['WOProdSpecID', 'InvDescription', 'OpMachineNum',
            'OpWorkOrderID', 'SetID', 'OpFinishedByProduction', 'SetLengthFt',
            'Setup per Set', 'Run per Set', 'Down per Set', 'Labor per Set',
            'Splice Count', 'Setup']
        filters = ['CustomerCode', 'InvDescription', 'OpMachineNum']

        self.mdf = self.df[columns]


    # Assume WO in Metrics and WO + sets in Schedule are chronological
