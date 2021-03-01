'''Display graphs & app controls.'''
from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase

import time
import numpy as np
import tkinter as tk
from tkinter import ttk


class GraphView(SinkBase):
    '''A sink node to display the graphs.'''
    engagement = False
    keyboard = False
    mouse = False

    def __init__(self, mouse_source: SourceBase,
                 keyboard_source: SourceBase,
                 engagement_source: SourceBase, interval=0.1, history=5):
        '''Return periodically redrawing FigureCanvasTkAgg'''

        self.engagement = False
        self.keyboard = False
        self.mouse = False
        self.interval = interval
        self.history = history

        mouse_source.get_data_stream().subscribe(self.display_mouse_event)
        keyboard_source.get_data_stream().subscribe(self.display_key_event)
        engagement_source.get_data_stream().subscribe(self.display_engagement)

        self.plot()

    def plot(self):
        '''Start plotting loop'''
        length = self.history / self.interval
        points = np.zeros((length, 2))

        while 1:
            time.sleep(.5)
            points = points[-length:]
            points = np.append(points, [[0, 0]], 0)

            if self.engagement:
                points[-1, 0] = 1
                self.engagement = False
            if self.keyboard or self.mouse:
                points[-1, 1] = 1
                self.keyboard = False
                self.mouse = False

    def display_engagement(self, code: int):
        '''Register appropriate engagement level change'''
        self.engagement = code < 2

    def display_key_event(self):
        '''Register keyboard event'''
        self.keyboard = True

    def display_mouse_event(self):
        '''Register mouse event'''
        self.mouse = True
