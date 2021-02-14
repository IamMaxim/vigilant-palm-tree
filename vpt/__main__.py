'''Main entry point for the package'''
from vpt.cli import parse_args
from vpt.sources import print_audio_inputs

args = parse_args()

if args['cmd'] == 'sources':
    if args['source'] == 'audio':
        print_audio_inputs()
    elif args['source'] == 'video':
        pass
