'''A group of functions to make sure the hardware is correctly functioning
    and recognized by the program.'''
import json
import time

import keyboard
import mouse
import sounddevice as sd
import soundfile as sf

from vpt.processors.gaze_detector import GazeDetector
from vpt.sinks import VideoDisplay, FileStore
from vpt.sources import DeviceVideoSource, KeyboardSource, MouseSource, DeviceAudioSource


def record_audio(device=None, duration=5, filename='vpt-audio.wav'):
    '''Records audio from the given device and saves it to disk.
       Note that it currently blocks the main thread for the given duration.'''
    if device is None:
        device = sd.query_devices(kind='input')
    else:
        device = sd.query_devices(device)

    samplerate = int(device['default_samplerate'])
    channels = min(2, device['max_input_channels'])

    sd.default.samplerate = samplerate
    sd.default.channels = channels

    data = sd.rec(int(samplerate * duration))
    sd.wait()
    with sf.SoundFile(filename, mode='w', samplerate=samplerate, channels=channels) as file:
        file.write(data)


def record_mouse(duration=5, filename='vpt-mouse.json'):
    '''Records all mouse events and saves them to a JSON file.
       Note that it currently blocks the main thread for the given duration.'''
    events = []

    def callback(event):
        if isinstance(event, mouse.ButtonEvent):
            events.append({
                'type': 'button',
                'button': event.button,
                'action': event.event_type,
                'time': event.time,
            })
        elif isinstance(event, mouse.WheelEvent):
            events.append({
                'type': 'wheel',
                'delta': event.delta,
                'time': event.time,
            })
        elif isinstance(event, mouse.MoveEvent):
            events.append({
                'type': 'move',
                'position': {
                    'x': event.x,
                    'y': event.y,
                },
                'time': event.time,
            })

    mouse.hook(callback)
    time.sleep(duration)
    mouse.unhook(callback)
    with open(filename, 'w') as file:
        json.dump(events, file, indent=4)


def record_keyboard(duration=5, filename='vpt-keyboard.json'):
    '''Record all keyboard events and save them to a json file
       Note that it currently blocks the main thread for the given duration.'''
    events = []

    def callback(event: keyboard.KeyboardEvent):
        events.append({
            'character': event.name,
            'key_code': event.scan_code,
            'time': event.time,
        })

    keyboard.hook(callback)
    time.sleep(duration)
    keyboard.unhook(callback)
    with open(filename, 'w') as file:
        json.dump(events, file, indent=4)


def check():
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
    gaze_detector.get_data_stream().subscribe(lambda v: print(v))

    # Run UI on the MainThread (this is a blocking call)
    video_display.run()

    # Stop capture on all types of sources
    video_source.stop()
    audio_source.stop()
    keyboard_source.stop()
    mouse_source.stop()

    print('Done')
