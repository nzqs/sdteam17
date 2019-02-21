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
        self.df = pd.DataFrame() # Master df
        self.datadict = {
            # Sample attributes
            # 'processing_time': [],
            # 'thaw_time': []
            }
        self.datadf = pd.DataFrame() # Parsed df

    # Open Excel file and read given sheet. Assume headers on second row.
    def read_file(self, file_name, sheet_name, header = 1):
        self.df = pd.read_excel(file_name, sheet_name = sheet_name, header = header)

    def write_data(self, out_file = "Web Data.csv"):
        # TODO: Read df, parse necessary values and dump
        # out_file is file name
        # Placeholder implementation. Real values should be in a DataFrame
        self.datadf.to_csv(out_file, index = False)

    def gen_id(self, *argv):
        # Combine given *args columns into a new column. Use parsed df.
        # Concatenate as strings. Avoids unwanted arithmetic
        # Gen empty col, default value None, then
        # df.id = df.id + df.arg for arg in args
        self.datadf['id'] = ''
        for arg in argv:
            self.datadf['id'] = self.datadf['id'].astype(str) + self.datadf[str(arg)].astype(str)

    def write_data(self, out_file):
        # TODO: Read df, parse necessary values and dump
        # out_file is file name
        # Placeholder implementation. Real values should be in a DataFrame
        self.datadf.to_excel(index = False)
        pass

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
            'start_time', 'end_time', 'thaw_time', 'pull_time']
        self.datadf = pd.DataFrame(columns = columns)
        self.datadf.work_order, self.datadf.set_number, self.datadf.start_time, self.datadf.end_time = self.df.WO, self.df.Set, self.df.Start, self.df.Finish
        self.datadf.part_number, self.datadf.pull_time = self.df.PN, self.df['Pull Material']
        # Coerce datetime columns to datetime type.
        # Sounds redundant, but this lets us handle empty or invalid data
        self.df.Start = self.df.Start.apply(pd.to_datetime, errors = 'coerce')
        self.df.Finish = pd.to_datetime(arg = self.df.Finish, errors = 'coerce')
        self.df['Pull Material'] = pd.to_datetime(self.df['Pull Material'], errors = 'coerce')
        #    'start_time', 'end_time', 'thaw_time']
        self.datadf = pd.DataFrame(columns = columns)
        self.datadf.work_order, self.datadf.set_number, self.datadf.start_time, self.datadf.end_time = self.df.WO, self.df.Set, self.df.Start, self.df.Finish
        self.datadf.part_number = self.df.PN
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
        self.datadf.drop(self.datadf[self.datadf.processing_time < pd.Timedelta('0 days')].index, inplace = True)
        # Drop duplicate header rows
        # self.datadf.drop(self.datadf[self.datadf.set_number == 'Set'].index, inplace = True)
        self.datadf = self.datadf[self.datadf.set_number != 'Set']
        # Remove blank rows
        self.datadf.dropna(how = 'all', inplace = True)
        # Remove 2001 values from MC12. For now, remove all before 2016
        self.datadf.drop(self.datadf[self.datadf.start_time < pd.to_datetime('2016-01-01')].index, inplace = True)
        # Find hours of processing time. Modify in place for now.
        self.datadf.processing_time = self.datadf.processing_time / pd.np.timedelta64(1, 'h')
        self.datadf.thaw_time = self.datadf.thaw_time / pd.np.timedelta64(1, 'h')
        # Drop some strange bogus rows with no start or end time
        self.datadf.dropna(subset = ['start_time', 'end_time'], inplace = True)

    def merge_workorder(self):
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
        # Define resource function for color coding
        is_downtime = lambda row: 'Downtime' if row['work_order'] in downtime_column else 'Job'
        wodf['Resource'] = wodf.apply(is_downtime, axis = 1)
        return wodf

class WebExcelMetrics(WebExcel):
    """
    Subclass of WebExcel
    Implement methods to handle the Metrics files
    """
    # Assume WO in Metrics and WO + sets in Schedule are chronological
    def __init__(self):
        super(WebExcelMetrics, self).__init__()

    def parse_metrics(self):
        columns = ['WOProdSpecID', 'CustomerCode','InvDescription', 'OpMachineNum',
            'OpWorkOrderID', 'SetID', 'OpFinishedByProduction', 'SetLengthFt',
            'Setup per Set', 'Run per Set', 'Down per Set', 'Labor per Set',
            'Splice Count', 'Setup']
        self.datadf = self.df[columns]
        # Count the number of sets
        self.datadf['SetNum'] = self.datadf.groupby('OpWorkOrderID').cumcount()

    def filters(self):
        # Filter for MC12, MC28, client
        self.datadf = self.datadf.loc[self.datadf['CustomerCode'].isin(['Hexc01', 'Hexc04', 'Hexc05'])]
        self.datadf = self.datadf.loc[self.datadf['OpMachineNum'].isin([12,14])]

class WebExcelHelper(object):
    """
    Helper class for WebExcel.
    Odds and ends for operations that don't belong in other classes.
    """
    def __init__(self):
        super(WebExcelHelper, self).__init__()
        self.placeholder = None

    @staticmethod
    def merge_schedule_metrics(df1, df2):
        df = df1.join(df2.set_index('id'), on = 'id')
        return df
        wodf = wodf.sort_values(by = 'start_time')
        return wodf
        # if WO not in set(seen WO):
        #   df[df.WO == WO].first.start + df[df.WO == WO].last.finish
