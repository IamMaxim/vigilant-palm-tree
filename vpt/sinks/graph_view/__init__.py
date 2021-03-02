'''Display graphs & app controls.'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase


class GraphView(SinkBase):
    '''A sink node to display the graphs.'''

    def __init__(self, mouse_source: SourceBase,
                 keyboard_source: SourceBase,
                 engagement_source: SourceBase):
        '''Add periodically redrawing canvas to TkWindow'''

        self.engagement = False
        self.keyboard = False
        self.mouse = False

        mouse_source.get_data_stream().subscribe(self.catch_mouse_event)
        keyboard_source.get_data_stream().subscribe(self.catch_key_event)
        # engagement_source.get_data_stream().subscribe(self.catch_engagement)

    def run(self,  interval=0.1, history=5):
        '''Start plotting loop'''
        _fig, axs = plt.subplots(
            1, 2, sharex=True, sharey=True, figsize=(5, 5))

        n = int(history / interval)
        xs = list(range(n))
        points = np.random.randint(0, 2, (n, 2))

        while 1:
            points = np.append(points, np.random.randint(0, 2, (1, 2)), 0)[-n:]
            # points = np.append(points, [[0, 0]], 0)[-n:]

            if self.engagement:
                points[-1, 0] = 1
                self.engagement = False
            if self.keyboard or self.mouse:
                points[-1, 1] = 1
                self.keyboard = False
                self.mouse = False

            self.plot(xs, points[:, 0], axs[0], "Mouse & Keyboard input")
            self.plot(xs, points[:, 1], axs[1], "Engagement")

            Button(plt.axes([0.9, 0.0, 0.1, 0.075]),
                   'Stop recording').on_clicked(lambda: print("Stop recording"))

            plt.ioff()
            plt.pause(interval)

    def plot(self, xs, ys, axs, title):
        '''Plot points on the axis'''
        axs.cla()
        axs.set_title(
            title + (" (present)" if ys[-1] else " (absent)"), fontsize=10)
        axs.axis('off')
        axs.bar(xs, ys, 1)

    def catch_engagement(self, code: int):
        '''Register appropriate engagement level change'''
        self.engagement = code < 2

    def catch_key_event(self):
        '''Register keyboard event'''
        input("key event")
        self.keyboard = True

    def catch_mouse_event(self):
        '''Register mouse event'''
        input("mouse event")
        self.mouse = True
