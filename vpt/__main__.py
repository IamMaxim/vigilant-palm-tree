"""Main entry point for the package"""
from vpt.cli.check import check
from vpt.cli.cli import parse_args
from vpt.cli.record import record
from vpt.cli.sources import print_audio_inputs, print_video_inputs, get_default_audio_input_index

args = parse_args(audio_default=get_default_audio_input_index())

if args['cmd'] == 'sources':
    if args['source'] == 'audio':
        print_audio_inputs()
    elif args['source'] == 'video':
        print_video_inputs()
elif args['cmd'] == 'check':
    check()
elif args['cmd'] is None:
    # If no argument, fall back to recording
    record(int(args['audio']), args['video'])
