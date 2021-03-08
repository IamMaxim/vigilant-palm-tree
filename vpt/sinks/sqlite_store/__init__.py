'''The SQLite store is responsible for writing streams to an SQLite database.'''
import sqlite3
import threading
import time
from queue import Queue
from typing import Union

import keyboard
import mouse

from data_structures import Engagement
from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase


class SQLiteStore(SinkBase):
    """Persistently store the engagement level and keyboard/mouse events
       in an SQLite database."""

    lock = threading.Lock()

    # mouse_queue: queue.Queue[Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]]
    mouse_queue: Queue
    # keyboard_queue: queue.Queue[keyboard.KeyboardEvent]
    keyboard_queue: Queue
    # engagement_queue: queue.Queue[int]
    engagement_queue: Queue

    connection: sqlite3.Connection

    def __init__(self, db_path: str, mouse_source: SourceBase,
                 keyboard_source: SourceBase, engagement_source: SourceBase):
        """Create a database or open an existing one."""
        self.stopped = True
        self.sources = [mouse_source, keyboard_source, engagement_source]
        self.connection = sqlite3.connect(db_path)

        self.engagement_queue = Queue()
        self.keyboard_queue = Queue()
        self.mouse_queue = Queue()

        # Create tables
        cur = self.connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS engagement (
                code integer NOT NULL,
                timestamp integer NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS keystrokes (
                type text NOT NULL,
                scancode integer NOT NULL,
                modifiers text NOT NULL,
                timestamp integer NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS mouse_events (
                type text NOT NULL,
                x integer,
                y integer,
                wheel_delta integer,
                button text,
                timestamp integer NOT NULL
            )
        ''')
        self.connection.commit()
        cur.close()

        mouse_source.output.subscribe(self.save_mouse)
        keyboard_source.output.subscribe(self.save_keyboard)
        engagement_source.output.subscribe(self.save_engagement)

    def __del__(self):
        """Clean up resources."""
        self.connection.commit()
        self.connection.close()

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

    def store_engagement(self, code: int):
        """Store an instance of engagement."""
        with self.lock:
            cur = self.connection.cursor()
            cur.execute('''
                INSERT INTO engagement VALUES (?, ?)
            ''', (code, int(time.time())))
            self.connection.commit()
            cur.close()

    def store_key_event(self, event: keyboard.KeyboardEvent):
        """Store a keypress with all of its modifiers."""
        with self.lock:
            cur = self.connection.cursor()
            cur.execute('''
                INSERT INTO keystrokes VALUES (?, ?, ?, ?)
            ''', (
                event.event_type,
                event.scan_code,
                ','.join(event.modifiers) if event.modifiers is not None else ''
                , int(event.time)
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
