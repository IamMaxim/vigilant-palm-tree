import sqlite3
import time
from typing import Union

import keyboard
import mouse

from nodes import SinkBase


class SQLiteStore(SinkBase):
    '''Persistently store the engagement level and keyboard/mouse events
       in an SQLite database.'''
    connection: sqlite3.Connection

    def __init__(self, db_path: str):
        '''Create a database or open an existing one.'''
        self.connection = sqlite3.connect(db_path)
        c = self.connection.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS engagement (
                code integer NOT NULL,
                timestamp integer NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS keystrokes (
                keycode integer NOT NULL,
                modifiers text NOT NULL,
                timestamp integer NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS mouse_events (
                type text NOT NULL,
                x real,
                y real,
                delta integer,
                button text,
                timestamp integer NOT NULL
            )
        ''')
        self.connection.commit()
        c.close()

    def __del__(self):
        '''Clean up resources.'''
        self.connection.commit()
        self.connection.close()

    def store_engagement(self, code: int):
        '''Store an instance of engagement.'''
        c = self.connection.cursor()
        c.execute('''
            INSERT INTO engagement VALUES (?, ?)
        ''', (code, int(time.time())))
        self.connection.commit()
        c.close()

    def store_key_event(self, event: keyboard.KeyboardEvent):
        '''Store a keypress with all of its modifiers.'''
        c = self.connection.cursor()
        c.execute('''
            INSERT INTO keystrokes VALUES (?, ?, ?)
        ''', (event.scan_code, ','.join(modifiers), int(event.time)))
        self.connection.commit()
        c.close()

    def store_mouse_event(self, event: Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]):
        '''Store mouse movements, button presses and scrolls.'''
        c = self.connection.cursor()
        if isinstance(event, mouse.MoveEvent):
            c.execute('''
                INSERT INTO mouse_events VALUES (?, ?, ?, NULL, NULL, ?)
            ''', ('move', event.x, event.y, int(event.time)))
        elif isinstance(event, mouse.WheelEvent):
            c.execute('''
                INSERT INTO mouse_events VALUES (?, NULL, NULL, ?, NULL ?)
            ''', ('wheel', event.delta, int(event.time)))
        else:
            c.execute('''
                INSERT INTO mouse_events VALUES (?, NULL, NULL, NULL, ?, ?)
            ''', ('button', f'{event.button}:{event.event_type}'))
        self.connection.commit()
        c.close()
