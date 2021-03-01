'''A group of functions to make sure the hardware is correctly functioning
    and recognized by the program.'''
import sounddevice as sd

from vpt.processors.gaze_detector import GazeDetector
from vpt.sinks import VideoDisplay, FileStore
from vpt.sources import DeviceVideoSource, KeyboardSource, MouseSource, DeviceAudioSource


def check():
    '''Runs all of the recorders to check that everything works correctly.'''
    print('Checking the devices for 5s...')

    # Create capture nodes
    video_source = DeviceVideoSource()
    audio_source = DeviceAudioSource()
    keyboard_source = KeyboardSource()
    mouse_source = MouseSource()

    # Create GUI nodes
    video_display = VideoDisplay(video_source, duration=5)

    # Create file output nodes
    FileStore('.', mouse_source, keyboard_source, audio_source)

    # Start capture on all types of sources
    video_source.start()
    audio_source.start()
    keyboard_source.start()
    mouse_source.start()

    gaze_detector = GazeDetector(video_source)
    gaze_detector.get_data_stream().subscribe(print)

    # Run UI on the MainThread (this is a blocking call)
    video_display.run()

    # Stop capture on all types of sources
    video_source.stop()
    audio_source.stop()
    keyboard_source.stop()
    mouse_source.stop()

    print('Done')
