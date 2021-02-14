'''Main entry point for the package'''
from vpt.cli import parse_args
from vpt.sources import print_audio_inputs, print_video_inputs, get_default_audio_input_name
from vpt.check import record_audio, record_mouse

args = parse_args(audio_default=get_default_audio_input_name())

if args['cmd'] == 'sources':
    if args['source'] == 'audio':
        print_audio_inputs()
    elif args['source'] == 'video':
        print_video_inputs()
elif args['cmd'] == 'check':
    print(f'Recording duration: {args["duration"]} s')
    print('* Recording audio...')
    record_audio(device=args['audio'], duration=args['duration'])
    print('* Recording mouse...')
    record_mouse(duration=args['duration'])
    print('Done')
