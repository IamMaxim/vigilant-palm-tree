"""Display graphs & app controls."""
import time
from typing import Union
from collections import deque

import keyboard
import mouse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from rx import operators
from rx.scheduler.mainloop import QtScheduler
from matplotlib.backends.backend_qt5agg import QtWidgets, FigureCanvas

from vpt.capabilities import OutputCapable
from vpt.sinks.base import SinkBase
from vpt.data_structures import Engagement


class GraphView(SinkBase):
    """A sink node to display the graphs."""

    def __init__(self,
                 mouse_source: OutputCapable[
                     Union[mouse.MoveEvent, mouse.WheelEvent, mouse.ButtonEvent]
                 ],
                 keyboard_source: OutputCapable[keyboard.KeyboardEvent],
                 engagement_source: OutputCapable[Engagement]):
        self.stopped = True
        self.sources = [mouse_source, keyboard_source, engagement_source]
        self.window = None
        self.last_keyboard_time = 0
        self.last_mouse_time = 0
        self.points_in_buffer = 20
        self.buffer = deque([(0, 0)] * self.points_in_buffer, maxlen=self.points_in_buffer)

    def start(self):
        if not self.stopped:
            return
        super().start()
        mouse_source, keyboard_source, engagement_source = self.sources

        initial_keyboard_event = keyboard.KeyboardEvent(keyboard.KEY_UP, 0)
        initial_mouse_event = mouse.ButtonEvent(event_type=mouse.UP,
                                                button=0,
                                                time=time.time())
        self.subscriptions = [
            mouse_source.output.pipe(operators.start_with(initial_mouse_event))
                .pipe(operators.combine_latest(
                    keyboard_source.output.pipe(operators.start_with(initial_keyboard_event)),
                    engagement_source.output
                ))
                .pipe(operators.throttle_first(0.1))  # in seconds
                .subscribe(self.update)
        ]

        if self.window is None:
            self.window = Window(points=self.points_in_buffer,
                                 toggle_callback=self.toggle_recording)

        self.window.show()
        self.window.activateWindow()
        self.window.raise_()

    def toggle_recording(self):
        '''Change button text'''
        if not self.stopped:
            self.stop()
        else:
            self.start()

    def narrow_data(self, data):
        '''Get 2 points 0/1 from data.'''
        point = [0, 0]
        if data:
            mouse, keyboard, engagement = data

            kb_event = self.last_keyboard_time != keyboard.time
            ms_event = self.last_mouse_time != mouse.time

            if kb_event:
                self.last_keyboard_time = keyboard.time
            if ms_event:
                self.last_mouse_time = mouse.time
            is_engaged = engagement in (
                Engagement.ENGAGEMENT, Engagement.CONFERENCING)

            point = [kb_event or ms_event, is_engaged]
        return point

    def update(self, data):
        '''Apply events and redraw'''
        point = self.narrow_data(data)
        self.buffer.append(point)
        self.window.plot(self.buffer)

class Window(QtWidgets.QMainWindow):
    '''Graph frontend window'''

    def __init__(self, points: int, toggle_callback):
        super().__init__()
        _main = QtWidgets.QWidget()
        self.setCentralWidget(_main)
        layout = QtWidgets.QVBoxLayout(_main)

        record_button = QtWidgets.QPushButton("Start/stop recording")
        record_button.clicked.connect(toggle_callback)
        layout.addWidget(record_button)

        figure, [self.axs_inp, self.axs_eng] = plt.subplots(
            1, 2, sharex=True, sharey=True, figsize=(5, 2))

        self.canvas = FigureCanvas(figure)
        layout.addWidget(self.canvas)

        self.points = points
        self.axs_inp.set_title("Input (keyboard/mouse)", fontsize=10)
        self.set_axis_ticks(self.axs_inp)
        self.axs_eng.set_title("Engagement", fontsize=10)
        self.set_axis_ticks(self.axs_eng)

        self.line_inp, *_ = self.axs_inp.plot(range(self.points), np.zeros(self.points))
        self.line_eng, *_ = self.axs_eng.plot(range(self.points), np.zeros(self.points))

    @staticmethod
    def set_axis_ticks(axis: Axes):
        axis.set_ylim(-0.2, 1.2)
        axis.set_yticks([0, 1])
        axis.set_yticklabels(["absent", "present"])
        axis.set_xticks([])

    def plot(self, ys):
        '''Update points'''
        self.line_inp.set_data(range(self.points), [i[0] for i in ys])
        self.line_eng.set_data(range(self.points), [i[1] for i in ys])
        self.canvas.draw_idle()
