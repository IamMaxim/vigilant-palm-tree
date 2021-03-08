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
                 engagement_source: SourceBase):

        self.app, self.qapp = self.init_window()

        self.last_keyboard_time = 0
        self.last_mouse_time = 0
        self.data = []
        self.max_points = 32
        self.points = np.empty((0, 2))

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

    def init_window(self):
        '''Create QT Window'''
        qapp = QtWidgets.QApplication.instance()
        if not qapp:
            qapp = QtWidgets.QApplication(sys.argv)

        app = Window()
        app.show()
        app.activateWindow()
        app.raise_()

        self._timer = app.canvas.new_timer(50)
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

    def update(self):
        '''Apply events and redraw'''
        print("Rerendering")
        if not self.data:
            return
        try:
            mouse, keyboard, engagement = self.data

            kb_event = self.last_keyboard_time != keyboard.time
            ms_event = self.last_mouse_time != mouse.time

            if kb_event:
                self.last_keyboard_time = keyboard.time

            if ms_event:
                self.last_mouse_time = mouse.time

            is_engaged = engagement in (
                Engagement.ENGAGEMENT, Engagement.CONFERENCING)

            self.points = np.concatenate((self.points, np.array([kb_event or ms_event, is_engaged]).reshape(1, 2)),
                                         axis=0)

            # Truncate the data to self.max_points latest values
            if self.points.shape[0] > self.max_points:
                self.points = self.points[self.points.shape[0] -
                                          self.max_points: self.points.shape[0], :]

            # start_recording = Button(self.axs[0][1], 'Start rec')
            # start_recording.on_clicked(self.start_recording_callback)
            # stop_recording = Button(self.axs[0][1], 'Stop rec')
            # stop_recording.on_clicked(self.stop_recording_callback)

            # self.plot(self.points[:, 0], self.axs[1]
            #           [0], "Input (mouse/keyboard)")
            # self.plot(self.points[:, 1], self.axs[1][1], "Engagement")
            self.app.plot(self.points[:, 0])
        except AttributeError:
            # No data yet
            pass


class 

class Window(QtWidgets.QMainWindow):
    '''Graph frontend'''

    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        push = QtWidgets.QPushButton("push me")
        layout.addWidget(push)

        self.fig, [self.axs, _] = plt.subplots(
            1, 2, sharex=True, sharey=True, figsize=(5, 2))

        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.axs.set_title("Input", fontsize=10)
        self._line, *_ = self.axs.plot([0], [0])

        # # self._dynamic_ax = self.fig.subplots()
        # # self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))

        # self._timer = dynamic_canvas.new_timer(50)
        # self._timer.add_callback(self._update_canvas)
        # self._timer.start()

    def plot(self, points):
        '''Update points'''
        self._line.set_data(range(len(points)), points)
        self.fig.canvas.draw()


# if __name__ == "__main__":
#     # Check whether there is already a running QApplication (e.g., if running
#     # from an IDE).
#     qapp = QtWidgets.QApplication.instance()
#     if not qapp:
#         qapp = QtWidgets.QApplication(sys.argv)

#     app = ApplicationWindow()
#     app.show()
#     app.activateWindow()
#     app.raise_()
#     qapp.exec_()
