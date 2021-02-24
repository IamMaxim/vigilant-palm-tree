'''The file store is responsible for writing streams to files.'''
import os
import contextlib
from pathlib import Path
from typing import Union

import keyboard
import mouse
import numpy as np
import soundfile as sf

from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase


class FileStore(SinkBase):
    '''A sink node that writes the input streams to a file.'''
    def __init__(self, dir_name: str, mouse_source: SourceBase,
                 keyboard_source: SourceBase, audio_source: SourceBase):
        super().__init__()
        self.dir = Path(dir_name)

        self.mouse_file = open(self.dir / 'mouse_output.txt', 'w+', buffering=1)
        mouse_source.get_data_stream().subscribe(self._process_mouse)

        self.keyboard_file = open(self.dir / 'keyboard_output.txt', 'w+', buffering=1)
        keyboard_source.get_data_stream().subscribe(self._process_key)

        with contextlib.suppress(FileNotFoundError):
            os.remove(self.dir / 'audio.wav')
        self.audio_file = sf.SoundFile(self.dir / 'audio.wav',
                                       mode='w', samplerate=44100, channels=1)
        audio_source.get_data_stream().subscribe(self._process_audio)

    def _process_audio(self, frame: np.ndarray):
        '''Write the audio frame to its file'''
        self.audio_file.write(frame)

    def _process_key(self, event: keyboard.KeyboardEvent):
        '''Write the keyboard event to its file'''
        self.keyboard_file.write(f'{event.event_type} {event.name} {event.scan_code} {event.time}\n')

    def _process_mouse(self, event: Union[mouse.ButtonEvent, mouse.MoveEvent, mouse.WheelEvent]):
        '''Write the mouse event to its file'''
        if isinstance(event, mouse.ButtonEvent):
            self.mouse_file.write(f'button {event.button} {event.event_type} {event.time}\n')
        elif isinstance(event, mouse.WheelEvent):
            self.mouse_file.write(f'wheel {event.delta} {event.time}\n')
        elif isinstance(event, mouse.MoveEvent):
            self.mouse_file.write(f'move {event.x} {event.y} {event.time}\n')
