'''The file store is responsible for writing streams to files.'''
import os
import contextlib
from pathlib import Path
from typing import Union

import keyboard
import mouse
import numpy as np
import soundfile as sf
from rx.scheduler.mainloop import QtScheduler

from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase


class FileStore(SinkBase):
    '''A sink node that writes the input streams to a file.'''

    def __init__(self, dir_name: str, mouse_source: SourceBase,
                 keyboard_source: SourceBase, audio_source: SourceBase):
        self.dir = Path(dir_name)
        self.stopped = True
        self.sources = [mouse_source, keyboard_source, audio_source]
        self.subscriptions = None

        self.mouse_file = open(self.dir / 'mouse_output.txt', 'w+', buffering=1)

        self.keyboard_file = open(self.dir / 'keyboard_output.txt', 'w+', buffering=1)

        with contextlib.suppress(FileNotFoundError):
            os.remove(self.dir / 'audio.wav')
        self.audio_file = sf.SoundFile(self.dir / 'audio.wav',
                                       mode='w', samplerate=44100, channels=2)

    def start(self, scheduler: QtScheduler):
        if not self.stopped:
            return
        super().start(scheduler)
        mouse_source, keyboard_source, audio_source = self.sources

        self.subscriptions = [
            audio_source.output.subscribe(self.store_audio_frame, scheduler=scheduler),
            mouse_source.output.subscribe(self.store_mouse_event, scheduler=scheduler),
            keyboard_source.output.subscribe(self.store_key_event, scheduler=scheduler),
        ]

    def store_audio_frame(self, frame: np.ndarray):
        '''Write the audio frame to its file.'''
        self.audio_file.write(frame)

    def store_key_event(self, event: keyboard.KeyboardEvent):
        '''Write the keyboard event to its file.'''
        self.keyboard_file.write(
            f'{event.event_type} {event.name} {event.scan_code} {event.time}\n')

    def store_mouse_event(self, event: Union[mouse.ButtonEvent, mouse.MoveEvent, mouse.WheelEvent]):
        '''Write the mouse event to its file.'''
        if isinstance(event, mouse.ButtonEvent):
            self.mouse_file.write(f'button {event.button} {event.event_type} {event.time}\n')
        elif isinstance(event, mouse.WheelEvent):
            self.mouse_file.write(f'wheel {event.delta} {event.time}\n')
        elif isinstance(event, mouse.MoveEvent):
            self.mouse_file.write(f'move {event.x} {event.y} {event.time}\n')
