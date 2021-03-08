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
                 engagement_source: SourceBase, history=5, interval=.5):

        self.points_count = int(history / interval)
        self.app, self.qapp = self.init_window(interval)

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

    def init_window(self, interval):
        '''Create QT Window'''
        qapp = QtWidgets.QApplication.instance()
        if not qapp:
            qapp = QtWidgets.QApplication(sys.argv)

        app = Window(self.points_count)
        app.show()
        app.activateWindow()
        app.raise_()

        self._timer = app.canvas.new_timer(interval)
        self._timer.add_callback(self.update)
        self._timer.start()

        return app, qapp

    def update_data(self, data):
        '''Update event records'''
        self.data = data

    # def start_recording_callback(self):
    #     print('Started recording')
    #
    # def stop_recording_callback(self):
    #     print('Stopped recording')

    def narrow_data(self):
        '''Get 2 points 0/1 from data'''
        if not self.data:
            return [0, 0]
        mouse, keyboard, engagement = self.data

        kb_event = self.last_keyboard_time != keyboard.time
        ms_event = self.last_mouse_time != mouse.time

        if kb_event:
            self.last_keyboard_time = keyboard.time
        if ms_event:
            self.last_mouse_time = mouse.time
        is_engaged = engagement in (
            Engagement.ENGAGEMENT, Engagement.CONFERENCING)

        return [kb_event or ms_event, is_engaged]

    def update(self):
        '''Apply events and redraw'''
        try:
            # point = self.narrow_data()
            point = np.random.randint(0, 2, 2)
            # print(point)
            self.points = np.append(self.points, [point], 0)
            self.points = self.poits[-self.points_count:]
            self.app.plot(self.points[:, 0], self.points[:, 1])

            # start_recording = Button(self.axs[0][1], 'Start rec')
            # start_recording.on_clicked(self.start_recording_callback)
            # stop_recording = Button(self.axs[0][1], 'Stop rec')
            # stop_recording.on_clicked(self.stop_recording_callback)

            # self.plot(self.points[:, 0], self.axs[1]
            #           [0], "Input (mouse/keyboard)")
            # self.plot(self.points[:, 1], self.axs[1][1], "Engagement")

        except AttributeError:
            # No data yet
            pass


class Window(QtWidgets.QMainWindow):
    '''Graph frontend window'''

    def __init__(self, points_count):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        push = QtWidgets.QPushButton("push me")
        layout.addWidget(push)

        self.fig, [self.axs_inp, self.axs_eng] = plt.subplots(
            1, 2, sharex=True, sharey=True, figsize=(5, 2))

        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.axs_inp.set_title("Input(keyboard/mouse)", fontsize=10)
        self.axs_eng.set_title("Engagement", fontsize=10)

        self.line_inp, *_ = self.axs_inp.plot(range(points_count))
        self.line_eng, *_ = self.axs_eng.plot(range(points_count))

    def plot(self, inp_ys, eng_ys):
        '''Update points'''
        print("plotting", inp_ys)
        self.line_inp.set_data(inp_ys)
        self.line_eng.set_data(eng_ys)
        self.canvas.draw()
