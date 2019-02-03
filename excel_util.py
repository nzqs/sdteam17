import pandas as pd

class WebExcel(object):
    """
    WebExcel class for opening, reading, and parsing Web's excel files.
    Class initializes with default objects:
        df: Empty Pandas DataFrame object
        data: Dictionary with desired attributes as keys mapped to empty lists
            May need to be overwritten for needed attributes.
    """
    def __init__(self):
        super(WebExcel, self).__init__()
        self.df = pd.DataFrame()
        self.data = {
            'processing_time': [],
            'thaw_time': []
            }

    def read_file(self, file_name):
        self.df = pd.read_excel(file_name)

    def read_schedule(self):
        # Parse proposed schedule
        # Implement similar methods for differently formatted files
        # Take schedule file and parse for processing time, thaw time, and more
        # Pass these values into data
        # Psuedocode: data['processing-time'] = self.df.end_time - self.df.start_time

    def write_data(self, out_file):
        # TODO: Read df, parse necessary values and dump
        # out_file is file name
        # Placeholder implementation. Real values should be in data
        self.df.to_excel(index = False)
