from web_setup_due import schedule
from cmfs_jupyter import cmfs, p_star, save_cmfs

import sys
import json
import dill
import argparse
from collections import namedtuple
from datetime import datetime
from gooey import Gooey, GooeyParser

running = False

@Gooey(
    program_name = 'Web Industries Scheduling',
    image_dir = 'resources/images',
    navigation = 'TABBED',
    poll_external_updates = True)
def main():

    # Find pickles or make them if they don't exist
    try:
        with open('cmfs.pickle', 'rb') as cpickle:
            pickled_cmfs = dill.load(cpickle)
    except (EOFError, FileNotFoundError):
        with open('cmfs.pickle', 'wb') as wpickle:
            dill.dump(dict(), wpickle)
            pickled_cmfs = {}

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
        "Constrained programming scheduling tool",
        "Specify input and output parameters",
        gooey_options={
            'show_border': True,
            'columns': 3})
    io_group.add_argument(
        'Schedule_Input',
        default='',
        help='Input jobs Excel file',
        widget='FileChooser')
    io_group.add_argument(
        '--write_schedule',
        default = '',
        help = 'Write schedule to given path.')
    io_group.add_argument(
        '--sheet',
        default = 'Sample 1',
        help = 'Sheet to read')
    io_group.add_argument(
        '--processing',
        default = 'p*',
        help = 'Processing time column')
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
        "Config options",
        "Recommended values")
    # args_group.add_argument(
    #     '--truncate',
    #     action = 'store_true',
    #     default = True,
    #     help = 'Group sets into work orders')
    args_group.add_argument(
        '--truncate',
        widget = 'Dropdown',
        choices = ['Yes', 'No'],
        default = 'Yes')
    args_group.add_argument(
        '--start_time',
        default = str(datetime.now().replace(microsecond = 0))[:-3],
        help = 'Schedule start time. Follow the example format')
    args_group.add_argument(
        '--max_run',
        default = 300,
        type=int,
        help='Maximum model run time in seconds')
    args_group.add_argument(
        '--output_proto',
        default='',
        help='Write CP model to output (for debugging)')
    args_group.add_argument(
        '--preprocess_times',
        action = 'store_true',
        default=True,
        help='Preprocess setup times and durations')
    # args_group.add_argument_group(
    #     '--parameters',
    #     help = 'Optimization parameters')

    ############################################################################
    # CMFs
    cmf_parser = subs.add_parser(
        'CMF', help = 'Calculate CMFs and fractiles from historical data')
    cio_group = cmf_parser.add_argument_group(
        "Load or modify historical data",
        "Specify input and output parameters")
    cio_group.add_argument(
        'CMF_Input',
        default = '', # Schedule-FMI.xlsx
        help = 'Input Excel file with processing data',
        widget = 'FileChooser')
    cio_group.add_argument(
        '--sheet',
        default = 'FMI',
        help = 'Sheet with data')
    cio_group.add_argument(
        '--mat_col',
        default = 'Material Description',
        help = 'Material description column')
    cio_group.add_argument(
        '--mach_col',
        default = 'Mach #',
        help = 'Machine number column')
    cio_group.add_argument(
        '--estim_col',
        default = 'Estim. Run Time',
        help = 'Estimated run time column')
    cio_group.add_argument(
        '--actual_col',
        default = 'Actual Run Time',
        help = 'Actual running time column')

    ############################################################################
    # P Star
    p_star_parser = subs.add_parser(
        'p*', help = 'Alotted processing time that balances job earliness and job tardiness tradeoff.')
    pio_group = p_star_parser.add_argument_group(
        "Calculate balanced processing times",
        "Load historical data to find a processing time that balances the costs")
    p_star_parser.add_argument(
        'theta',
        default = 300,
        type = int,
        help = 'Cost per hour of job earliness')
    p_star_parser.add_argument(
        'delta',
        default = 30000,
        type = int,
        help = 'Cost of an exceed out time incident')
    cmf_keys = [str(key) for key in list(pickled_cmfs.keys())]
    p_star_parser.add_argument(
        'Material',
        help = 'Choose which material to examine',
        widget = 'Dropdown',
        choices = cmf_keys
        )

    args = PARSER.parse_args()
    # Since the gui has multiple options, we run code in try loops and simply pass all args to each function
    try:
        schedule(args)
    except AttributeError:
        pass
    try:
        save_cmfs(args)
    except AttributeError:
        pass
    try:
    # Holy crap what a roundabout way to get the cmf.
    # I regret using namedtuple for keys.
        material_cmf = pickled_cmfs[list(pickled_cmfs.keys())[cmf_keys.index(args.Material)]]
        key = list(pickled_cmfs.keys())[cmf_keys.index(args.Material)]
        mean = key.Mean
        delta = round((0.5 * args.delta) / (72 - 36 - mean), 2) # Rescale delta here. Easier to remove if needed
        p = round(p_star(material_cmf, mean, args.theta, delta)) # Round to integer for CP
        msg = \
        """
        For material {}:
        The estimted cost per hour of job earliness is ${}.
        The estimated cost per hour of job lateness is  ${}.
        The estimated allotted processing time balancing these costs is {} hours.
        """
        print(msg.format(key, args.theta, delta, p))
    except (ValueError, AttributeError):
        pass

    # print(type(args.theta), type(args.delta))
if __name__ == '__main__':
    if 'gooey-seed-ui' in sys.argv:
        try:
            with open('cmfs.pickle', 'rb') as read:
                pickled_cmfs = dill.load(read)
            # Dump the keys of historical cmfs into as json mapping to material
            # Required so we can dynamically update the dropdown menu without restarting
            # dang what a cool feature.
            print(json.dumps({'Material': [str(key) for key in list(pickled_cmfs.keys())] }))
        except (EOFError, FileNotFoundError):
            with open('cmfs.pickle', 'wb') as wpickle:
                dill.dump(dict(), wpickle)

    main()
