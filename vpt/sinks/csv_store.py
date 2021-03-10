'''The CSV store is responsible for writing streams to an CSV file.'''
import os
import csv
import time
from pathlib import Path
from typing import Union

import keyboard
import mouse
from rx.scheduler.mainloop import QtScheduler

from vpt.data_structures import Engagement
from vpt.capabilities import OutputCapable
from vpt.sinks.base import SinkBase


class CSVStore(SinkBase):
    """Persistently store the engagement level and keyboard/mouse events
       in a CSV file."""
    engagement_writer: csv.DictWriter
    mouse_writer: csv.DictWriter
    keyboard_writer: csv.DictWriter

    def __init__(self, data_dir: str,
                 mouse_source: OutputCapable[
                     Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]
                 ],
                 keyboard_source: OutputCapable[keyboard.KeyboardEvent],
                 engagement_source: OutputCapable[Engagement]):
        """Create a database or open an existing one."""
        self.stopped = True
        self.sources = [mouse_source, keyboard_source, engagement_source]
        self.subscriptions = None

        os.makedirs(data_dir, exist_ok=True)
        data_path = Path(data_dir)

        self.engagement_file = open(data_path / 'engagement.csv', 'w', newline='')
        self.mouse_file = open(data_path / 'mouse.csv', 'w', newline='')
        self.keyboard_file = open(data_path / 'keyboard.csv', 'w', newline='')

        self.engagement_writer = csv.DictWriter(self.engagement_file, ['code', 'timestamp'])
        self.engagement_writer.writeheader()
        self.mouse_writer = csv.DictWriter(self.mouse_file, ['type', 'x', 'y', 'wheel_delta',
                                                             'button', 'timestamp'])
        self.mouse_writer.writeheader()
        self.keyboard_writer = csv.DictWriter(self.keyboard_file, ['type', 'scancode', 'modifiers',
                                                                   'timestamp'])
        self.keyboard_writer.writeheader()

    def start(self):
        if not self.stopped:
            return
        super().start()
        mouse_source, keyboard_source, engagement_source = self.sources

        self.subscriptions = [
            mouse_source.output.subscribe(self.store_mouse_event),
            keyboard_source.output.subscribe(self.store_key_event),
            engagement_source.output.subscribe(self.store_engagement),
        ]

    def __del__(self):
        """Clean up resources."""
        self.engagement_file.close()
        self.mouse_file.close()
        self.keyboard_file.close()

    def store_engagement(self, code: Engagement):
        """Store an instance of engagement."""
        self.engagement_writer.writerow({'code': code.value, 'timestamp': int(time.time())})

    def store_key_event(self, event: keyboard.KeyboardEvent):
        """Store a keypress with all of its modifiers."""
        self.keyboard_writer.writerow({
            'type': event.event_type,
            'scancode': event.scan_code,
            'modifiers': ','.join(event.modifiers) if event.modifiers is not None else '',
            'timestamp': int(event.time),
        })

    def store_mouse_event(self, event: Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]):
        """Store mouse movements, button presses and scrolls."""
        if isinstance(event, mouse.MoveEvent):
            data = {
                'type': 'move',
                'x': event.x,
                'y': event.y,
                'timestamp': int(event.time),
            }
        elif isinstance(event, mouse.WheelEvent):
            data = {
                'type': 'wheel',
                'wheel_delta': event.delta,
                'timestamp': int(event.time),
            }
        else:
            data = {
                'type': 'button',
                'button': f'{event.button}:{event.event_type}',
                'timestamp': int(event.time),
            }
        self.mouse_writer.writerow(data)
