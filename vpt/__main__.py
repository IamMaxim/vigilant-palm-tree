"""Main entry point for the package"""
from vpt.check import check
from vpt.cli import parse_args
from vpt.sources import print_audio_inputs, print_video_inputs, get_default_audio_input_name

args = parse_args(audio_default=get_default_audio_input_name())

print(args)

if args['cmd'] == 'sources':
    if args['source'] == 'audio':
        print_audio_inputs()
    elif args['source'] == 'video':
        print_video_inputs()
elif args['cmd'] == 'check':
    check()
