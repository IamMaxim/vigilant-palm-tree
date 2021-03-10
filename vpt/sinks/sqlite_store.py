'''The SQLite store is responsible for writing streams to an SQLite database.'''
import csv
import time
import threading
from typing import Union
from queue import Queue

import keyboard
import mouse
from rx.scheduler.mainloop import QtScheduler

from vpt.data_structures import Engagement
from vpt.capabilities import OutputCapable
from vpt.sinks.base import SinkBase


class SQLiteStore(SinkBase):
    """Persistently store the engagement level and keyboard/mouse events
       in an SQLite database."""
    connection: csv.DictWriter

    lock = threading.Lock()

    def __init__(self, db_path: str,
                 mouse_source: OutputCapable[
                     Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]
                 ],
                 keyboard_source: OutputCapable[keyboard.KeyboardEvent],
                 engagement_source: OutputCapable[Engagement]):
        """Create a database or open an existing one."""
        self.stopped = True
        self.sources = [mouse_source, keyboard_source, engagement_source]
        self.csv_file = open('data/engagement.csv', 'w', newline='')
        self.connection = csv.DictWriter(self.csv_file, ['code', 'timestamp'])
        self.connection.writeheader()

        self.engagement_queue = Queue()
        # self.keyboard_queue = Queue()
        # self.mouse_queue = Queue()

        # Create tables
        # cur = self.connection.cursor()
        # cur.execute('''
        #     CREATE TABLE IF NOT EXISTS engagement (
        #         code integer NOT NULL,
        #         timestamp integer NOT NULL
        #     )
        # ''')
        # cur.execute('''
        #     CREATE TABLE IF NOT EXISTS keystrokes (
        #         type text NOT NULL,
        #         scancode integer NOT NULL,
        #         modifiers text NOT NULL,
        #         timestamp integer NOT NULL
        #     )
        # ''')
        # cur.execute('''
        #     CREATE TABLE IF NOT EXISTS mouse_events (
        #         type text NOT NULL,
        #         x integer,
        #         y integer,
        #         wheel_delta integer,
        #         button text,
        #         timestamp integer NOT NULL
        #     )
        # ''')
        # self.connection.commit()
        # cur.close()

    def start(self, scheduler: QtScheduler):
        if not self.stopped:
            return
        super().start(scheduler)
        mouse_source, keyboard_source, engagement_source = self.sources

        # mouse_source.output.subscribe(self.save_mouse, scheduler=scheduler)
        # keyboard_source.output.subscribe(self.save_keyboard, scheduler=scheduler)
        engagement_source.output.subscribe(self.store_engagement, scheduler=scheduler)

    def save_engagement(self, engagement: Engagement):
        with self.lock:
            self.engagement_queue.put(engagement.value)

    def save_keyboard(self, event: keyboard.KeyboardEvent):
        with self.lock:
            self.keyboard_queue.put(event)

    def save_mouse(self, event: Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]):
        with self.lock:
            self.mouse_queue.put(event)

    def update(self):
        while len(self.engagement_queue.queue) > 0:
            self.store_engagement(self.engagement_queue.get())
        while len(self.keyboard_queue.queue) > 0:
            self.store_key_event(self.keyboard_queue.get())
        while len(self.mouse_queue.queue) > 0:
            self.store_mouse_event(self.mouse_queue.get())

    def __del__(self):
        """Clean up resources."""
        self.connection.commit()
        self.connection.close()

    def store_engagement(self, code: int):
        """Store an instance of engagement."""
        with self.lock:
            self.connection.writerow({'code': code, 'timestamp': int(time.time())})

    def store_key_event(self, event: keyboard.KeyboardEvent):
        """Store a keypress with all of its modifiers."""
        with self.lock:
            cur = self.connection.cursor()
            cur.execute('''
                INSERT INTO keystrokes VALUES (?, ?, ?, ?)
            ''', (
                event.event_type,
                event.scan_code,
                ','.join(event.modifiers) if event.modifiers is not None else '', int(
                    event.time)
            ))
            self.connection.commit()
            cur.close()

    def store_mouse_event(self, event: Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]):
        """Store mouse movements, button presses and scrolls."""
        with self.lock:
            cur = self.connection.cursor()
            if isinstance(event, mouse.MoveEvent):
                cur.execute('''
                    INSERT INTO mouse_events VALUES (?, ?, ?, NULL, NULL, ?)
                ''', ('move', event.x, event.y, int(event.time)))
            elif isinstance(event, mouse.WheelEvent):
                cur.execute('''
                    INSERT INTO mouse_events VALUES (?, NULL, NULL, ?, NULL, ?)
                ''', ('wheel', event.delta, int(event.time)))
            else:
                cur.execute('''
                    INSERT INTO mouse_events VALUES (?, NULL, NULL, NULL, ?, ?)
                ''', ('button', f'{event.button}:{event.event_type}', int(event.time)))
            self.connection.commit()
            cur.close()
