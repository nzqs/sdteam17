import pandas as pd

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

    def read_schedule(self):
        # Parse proposed schedule
        # Implement similar methods for differently formatted files
        # Take schedule file and parse for processing time, thaw time, and more
        # Pass these values into data
        # Psuedocode: data['processing_time'] = self.df.end_time - self.df.start_time
        self.datadict['processing_time'] = self.df.Finish - self.df.Start
        self.datadict['thaw_time'] = self.df.Start - self.df["Pull Material"]

        columns = ['work_order','set_number', 'part_number', 'processing_time', 'thaw_time']
        self.datadf = pd.DataFrame(columns = columns)
        self.datadf.work_order, self.datadf.set_number = self.df.WO, self.df.Set
        self.datadf.part_number = self.df.PN
        self.datadf.processing_time = self.df.Finish - self.df.Start
        self.datadf.thaw_time = self.df.Start - self.df['Pull Material']

    def sanity_check(self):
        # Remove crazy values.
        # This implementation is currently only for schedule.
        # Others may be added as needed
        # Processing time can't be negative. Keep positive time deltas
        # self.datadf = self.datadf[self.datadf.processing_time > pd.Timedelta('0 days')]
        self.datadf.drop(self.datadf[self.datadf.processing_time > pd.Timedelta(days = 0)].index)
        # Set work order to downtime
        # May need to backfill some wo
        self.datadf.loc[self.datadf.work_order.isna(), "work_order"] = self.datadf[self.datadf.work_order.isna()].part_number

    def read_orders(self):
        # Placeholder to read client submitted 90 day schedule
        pass

    def read_tables(self):
        # Placeholder to read table of known values
        # Processing time per material, thaw time per material etc.
        pass

    def write_data(self, out_file):
        # TODO: Read df, parse necessary values and dump
        # out_file is file name
        # Placeholder implementation. Real values should be in a DataFrame
        self.datadf.to_excel(index = False)
        pass
