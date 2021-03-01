'''Display graphs & app controls.'''
from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase

import keyboard
import mouse
import time
from typing import Union

import tkinter as tk
from tkinter import ttk


class GraphView(SinkBase):
    '''A sink node to display the graphs.'''

    def __init__(self, mouse_source: SourceBase,
                 keyboard_source: SourceBase, engagement_source: SourceBase):

        mouse_source.get_data_stream().subscribe(self.display_mouse_event)
        keyboard_source.get_data_stream().subscribe(self.display_key_event)
        engagement_source.get_data_stream().subscribe(self.display_engagement)

    def display_engagement(self, code: int):
        '''Register engagement level change'''
        self.engagement = code < 2

    def display_key_event(self, event: keyboard.KeyboardEvent):
        '''Register keyboard event'''
        self.keyboard = True

    def display_mouse_event(self, event: Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]):
        '''Register mouse event'''
        self.mouse = True
