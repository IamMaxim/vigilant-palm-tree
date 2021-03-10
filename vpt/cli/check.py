'''A group of functions to make sure the hardware is correctly functioning
    and recognized by the program.'''
import sounddevice as sd
from rx.scheduler import ImmediateScheduler

from vpt.sinks import VideoDisplay, FileStore
from vpt.sources import DeviceVideoSource, KeyboardSource, MouseSource, DeviceAudioSource
from vpt.cli.cli import parse_args


def check():
    '''Runs all of the recorders to check that everything works correctly.'''
    args = parse_args(audio_default=sd.query_devices(kind='input')['name'])
    print('Checking the devices for 5s...')

    # Create capture nodes
    audio_device = sd.query_devices(kind='input', device=args['audio'])
    video_source = DeviceVideoSource(int(args['video']))
    audio_source = DeviceAudioSource(audio_device['max_input_channels'],
                                     audio_device['default_samplerate'],
                                     args['audio'])
    keyboard_source = KeyboardSource()
    mouse_source = MouseSource()

    # Create GUI nodes
    video_display = VideoDisplay(video_source, duration=5)

    # Create file output nodes
    file_store = FileStore('.', mouse_source, keyboard_source, audio_source)

    # Run UI on the MainThread (this is a blocking call)
    scheduler = ImmediateScheduler()
    file_store.start(scheduler)
    video_display.start(scheduler)

    # Stop capture on all types of sources
    file_store.stop()
    video_display.stop()

    print('Done')
