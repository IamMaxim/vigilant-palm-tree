import sys
from datetime import datetime
from argparse import ArgumentParser

parser = ArgumentParser(prog='vpt', description="A research tool that allows collecting "
        "audio/video data to predict a person's state of work engagement and correlate that "
        "data with that person's keyboard/mouse activity")
subparsers = parser.add_subparsers(dest='cmd')

check_parser = subparsers.add_parser('check', description='Make sure your hardware is correctly '
        'functioning and recognized by the program')

record_parser = subparsers.add_parser('record', description='Start recording the data')
record_parser.add_argument('--audio', help='The name of the audio source, as reported by the '
        '"sources audio" subcommand')
record_parser.add_argument('--video', help='The name of the audio source, as reported by the '
        '"sources video" subcommand')

sources_parser = subparsers.add_parser('sources', description='List all available sources')
sources_parser.add_argument('source', choices=['audio', 'video'])

report_parser = subparsers.add_parser('report', description='Generate a PDF report')

dump_parser = subparsers.add_parser('dump', description='Get a dataset of keyboard/mouse '
        'activity along with the predicted work state engagement levels from audio/video')
dump_parser.add_argument('-o', '--output', help='SQLite database file path', default='vpt-data.sql')

clear_parser = subparsers.add_parser('clear', description='Clear the data collected by the program')
clear_parser.add_argument('-s', '--start', type=datetime.fromisoformat,
                          help='Start date of the range whose data to delete')
clear_parser.add_argument('-e', '--end', type=datetime.fromisoformat,
                          help='Start date of the range whose data to delete')


args = parser.parse_args()

if args.cmd is None:
    parser.print_usage()
    sys.exit(-1)

print(args)
