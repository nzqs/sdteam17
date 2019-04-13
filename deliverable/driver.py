from web_setup_due import schedule
from cmfs_jupyter import cmfs, p_star

import argparse
import dill
from collections import namedtuple
from datetime import datetime
from gooey import Gooey, GooeyParser

running = False

@Gooey(program_name = 'Web Industries Scheduling', image_dir = 'resources/images', navigation = 'TABBED')
def main():

    # Find pickles or make them if they don't exist
    try:
        with open('cmfs.pickle', 'rb') as cpickle:
            pickled_cmfs = dill.load(cpickle)
    except EOFError:
        with open('cmfs.pickle', 'wb') as wpickle:
            dill.dump(dict(), wpickle)

    # Create empty pickles

    #----------------------------------------------------------------------------
    # Command line arguments.
    # Add a tabbed group for each different program functionality.
    PARSER = GooeyParser(description = 'Georgia Tech Senior Design Project' \
                                       'Author: Nicholas She ')
    PARSER.add_argument('--verbose', help='be verbose', dest='verbose',
                        action='store_true', default=False)
    subs = PARSER.add_subparsers(help = 'commands', dest = 'command')

    ############################################################################
    # Schedule
    sched_parser = subs.add_parser(
        'Schedule', help = 'Constrained programming scheduling tool')
    io_group = sched_parser.add_argument_group(
        "Input and output options",
        "Custom input and output files")
    io_group.add_argument(
        'Schedule_Input',
        default='',
        help='Input jobs Excel file',
        widget='FileChooser')
    io_group.add_argument(
        '--sheet',
        default = 'MC12SimData (2)',
        help = 'Sheet to read')
    io_group.add_argument(
        '--write_schedule',
        default = '',
        help = 'Write schedule to given path.')
    io_group.add_argument(
        '--processing',
        default = 'p*',
        help = 'Processing time column. May be deprecated')
    io_group.add_argument(
        '--WO',
        default = 'WO',
        help = 'Work order column')
    io_group.add_argument(
        '--set',
        default = 'Set',
        help = 'Set column')
    io_group.add_argument(
        '--material',
        default = 'Resin Type',
        help = 'Material or PN column')
    io_group.add_argument(
        '--width',
        default = 'Width',
        help = 'Width column')
    io_group.add_argument(
        '--due',
        default = 'Due Date',
        help = 'Due date column')

    args_group = sched_parser.add_argument_group(
        "Optional arguments",
        "Recommended values")
    args_group.add_argument(
        '--start_time',
        default = str(datetime.now().replace(microsecond = 0))[:-3],
        help = 'Schedule start time. Follow the example format')
    args_group.add_argument(
        '--max_run',
        default = 3600,
        type=int,
        help='Maximum model run time')
    args_group.add_argument(
        '--output_proto',
        default='',
        help='Output file to write the cp_model proto to.')
    args_group.add_argument(
        '--preprocess_times',
        action = 'store_true',
        default=True,
        help='Preprocess setup times and durations')
    args_group.add_argument(
        '--truncate',
        action = 'store_true',
        default = True,
        help = 'Process work orders only')
    # args_group.add_argument_group(
    #     '--parameters',
    #     help = 'Optimization parameters')

    ############################################################################
    # CMFs
    cmf_parser = subs.add_parser(
        'CMF', help = 'Calculate CMFs and fractiles from historical data')
    cmf_parser.add_argument(
        'CMF_Input',
        default = '',
        help = 'Input Excel file with processing data',
        widget = 'FileChooser')
    cmf_parser.add_argument(
        '--Material',
        default = '',
        help = 'Material to return CMF')
    cmf_parser.add_argument(
        '--sheet',
        default = 'FMI',
        help = 'Sheet with data')
    cmf_parser.add_argument(
        '--mat_col',
        default = 'Material Description',
        help = 'Material description column')
    cmf_parser.add_argument(
        '--mach_col',
        default = 'Mach #',
        help = 'Machine number column')
    cmf_parser.add_argument(
        '--estim_col',
        default = 'Estim. Run Time',
        help = 'Estimated run time column')
    cmf_parser.add_argument(
        '--actual_col',
        default = 'Actual Run Time',
        help = 'Actual running time column')

    args = PARSER.parse_args()
    try:
        schedule(args)
    except AttributeError:
        pass
    try:
        monty = cmfs(args)
        with open('cmfs.pickle', 'rb') as cpickle:
            pickled_cmfs = dill.load(cpickle)
        for key in monty.keys():
            pickled_cmfs[key] = monty[key]
        with open('cmfs.pickle', 'wb') as wpickle:
            dill.dump(pickled_cmfs, wpickle)
    except AttributeError:
        pass

if __name__ == '__main__':
    main()
