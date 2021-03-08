"""Display graphs & app controls."""
import time
import sys
import keyboard
import mouse
import numpy as np
import matplotlib.pyplot as plt

from rx import operators
from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase
from vpt.data_structures import Engagement

from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (FigureCanvas)
else:
    from matplotlib.backends.backend_qt4agg import (FigureCanvas)


class GraphView(SinkBase):
    """A sink node to display the graphs."""

    def __init__(self,
                 mouse_source: SourceBase,
                 keyboard_source: SourceBase,
                 engagement_source: SourceBase, history=5, interval=1):

        self.points_count = int(history / interval)
        self.app, self.qapp, self.record_button = self.init_window(
            history, interval)

        self.last_keyboard_time = 0
        self.last_mouse_time = 0
        self.data = False
        self.points = np.zeros((self.points_count, 2))

        initial_keyboard_event = keyboard.KeyboardEvent(keyboard.KEY_UP, 0)
        initial_mouse_event = mouse.ButtonEvent(
            event_type=mouse.UP, button=0, time=time.time())

        mouse_source.get_data_stream() \
            .pipe(operators.start_with(initial_mouse_event)) \
            .pipe(operators.combine_latest(
                keyboard_source.get_data_stream().pipe(
                    operators.start_with(initial_keyboard_event)),
                engagement_source.get_data_stream()
            )).subscribe(self.update_data)

        self.recording = False
        self.toggle_recording()

    def init_window(self, history, interval):
        '''Create QT Window'''
        qapp = QtWidgets.QApplication.instance()
        if not qapp:
            qapp = QtWidgets.QApplication(sys.argv)

        app = Window(self.points_count, history)

        record_button = QtWidgets.QPushButton("Paused")
        record_button.clicked.connect(self.toggle_recording)
        app.layout.addWidget(record_button)

        app.show()
        app.activateWindow()
        app.raise_()

        self._timer = app.canvas.new_timer(interval)
        self._timer.add_callback(self.update)
        self._timer.start()

        return app, qapp, record_button

    def toggle_recording(self):
        '''Change button text'''
        self.recording = not self.recording
        self.record_button.setText(
            'Recoding' if self.recording else 'Paused')

    def update_data(self, data):
        '''Update event records'''
        self.data = data
        # print("update data", data)

    # def start_recording_callback(self):
    #     print('Started recording')
    #
    # def stop_recording_callback(self):
    #     print('Stopped recording')

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

        # print('data point', point)
        return point

    def update(self):
        '''Apply events and redraw'''
        if not self.recording:
            return
        try:
            point = self.narrow_data()
            # point = np.random.randint(0, 2, 2)
            self.points = np.append(self.points, [point], 0)
            self.points = self.points[-self.points_count:]
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
            pass


class Window(QtWidgets.QMainWindow):
    '''Graph frontend window'''

    def __init__(self, n, history):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.layout = QtWidgets.QVBoxLayout(self._main)

        self.fig, [self.axs_inp, self.axs_eng] = plt.subplots(
            1, 2, sharex=True, sharey=True, figsize=(5, 2))

        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.axs_inp.set_title("Input (keyboard/mouse)", fontsize=10)
        self.set_axis(self.axs_inp, n, history)
        self.axs_eng.set_title("Engagement", fontsize=10)
        self.set_axis(self.axs_eng, n, history)

        self.n = n
        self.rn = range(n)

        self.line_inp, *_ = self.axs_inp.plot(self.rn, [0] * self.n)
        self.line_eng, *_ = self.axs_eng.plot(self.rn, [0] * self.n)

    def set_axis(self, ax, n, history):
        xlabels = [str(x)+'s' for x in [history, history/2, 0]]
        ax.set_xticks([0, n/2, n])
        ax.set_xticklabels(xlabels)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["absent", "present"])

    def plot(self, ys):
        '''Update points'''
        # print("plotting", ys)
        self.line_inp.set_data(self.rn, ys[:, 0])
        self.line_eng.set_data(self.rn, ys[:, 1])
        self.canvas.draw()
