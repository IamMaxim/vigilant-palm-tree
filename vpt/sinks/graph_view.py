"""Display graphs & app controls."""
import time
import sys
from typing import Union

import keyboard
import mouse
import numpy as np
import matplotlib.pyplot as plt
from rx import operators
from rx.scheduler.mainloop import QtScheduler
from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (FigureCanvas)
else:
    from matplotlib.backends.backend_qt4agg import (FigureCanvas)

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

    def start(self, scheduler: QtScheduler):
        if not self.stopped:
            return
        super().start(scheduler)
        mouse_source, keyboard_source, engagement_source = self.sources

        initial_keyboard_event = keyboard.KeyboardEvent(keyboard.KEY_UP, 0)
        initial_mouse_event = mouse.ButtonEvent(event_type=mouse.UP,
                                                button=0,
                                                time=time.time())
        mouse_source.output \
            .pipe(operators.start_with(initial_mouse_event)) \
            .pipe(operators.combine_latest(
                keyboard_source.get_data_stream().pipe(
                    operators.start_with(initial_keyboard_event)),
                engagement_source.get_data_stream()
            )).subscribe(self.update_data, scheduler=scheduler)

    def init_window(self, history, interval):
        '''Create QT Window.'''
        app = Window(self.max_points, history)

        record_button = QtWidgets.QPushButton("Paused")
        record_button.clicked.connect(self.toggle_recording)
        app.layout.addWidget(record_button)

        app.show()
        app.activateWindow()
        app.raise_()

        self._timer = app.canvas.new_timer(interval)
        self._timer.add_callback(self.update)
        self._timer.start()

        return app, record_button

    def toggle_recording(self):
        '''Change button text'''
        self.recording = not self.recording
        self.record_button.setText(
            'Recording' if self.recording else 'Paused')

    def update_data(self, data):
        '''Update event records'''
        self.data = data

    def narrow_data(self):
        '''Get 2 points 0/1 from data'''
        point = [0, 0]
        if self.data:
            mouse, keyboard, engagement = self.data

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

    def update(self):
        '''Apply events and redraw'''
        if not self.recording:
            return
        try:
            point = self.narrow_data()
            # point = np.random.randint(0, 2, 2)
            self.points = np.append(self.points, [point], 0)
            self.points = self.points[-self.max_points:]
            self.app.plot(self.points)

            # start_recording = Button(self.axs[0][1], 'Start rec')
            # start_recording.on_clicked(self.start_recording_callback)
            # stop_recording = Button(self.axs[0][1], 'Stop rec')
            # stop_recording.on_clicked(self.stop_recording_callback)

            # self.plot(self.points[:, 0], self.axs[1]
            #           [0], "Input (mouse/keyboard)")
            # self.plot(self.points[:, 1], self.axs[1][1], "Engagement")

        except AttributeError:
            # No data yet
            print("error in update")


class Window(QtWidgets.QMainWindow):
    '''Graph frontend window'''

    def __init__(self, n, history):
        super().__init__()
        _main = QtWidgets.QWidget()
        self.setCentralWidget(_main)
        layout = QtWidgets.QVBoxLayout(_main)

        figure, [self.axs_inp, self.axs_eng] = plt.subplots(
            1, 2, sharex=True, sharey=True, figsize=(5, 2))

        self.canvas = FigureCanvas(figure)
        layout.addWidget(self.canvas)

        self.axs_inp.set_title("Input (keyboard/mouse)", fontsize=10)
        self.set_axis(self.axs_inp, n, history)
        self.axs_eng.set_title("Engagement", fontsize=10)
        self.set_axis(self.axs_eng, n, history)

        self.n = n

        self.line_inp, *_ = self.axs_inp.plot(range(self.n), np.zeros(self.n))
        self.line_eng, *_ = self.axs_eng.plot(range(self.n), np.zeros(self.n))

    def set_axis(self, ax, n, history):
        xlabels = [str(x)+'s' for x in [history, history/2, 0]]
        ax.set_xticks([0, n/2, n])
        ax.set_xticklabels(xlabels)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["absent", "present"])

    def plot(self, ys):
        '''Update points'''
        self.line_inp.set_data(range(self.n), ys[:, 0])
        self.line_eng.set_data(range(self.n), ys[:, 1])
        self.canvas.draw()
