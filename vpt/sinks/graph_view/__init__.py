'''Display graphs & app controls.'''

import numpy as np
import matplotlib.pyplot as plt

from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase


class GraphView(SinkBase):
    '''A sink node to display the graphs.'''
    engagement = False
    keyboard = False
    mouse = False

    def __init__(self, mouse_source: SourceBase,
                 keyboard_source: SourceBase,
                 engagement_source: SourceBase, interval=0.1, history=5):
        '''Add periodically redrawing canvas to TkWindow'''

        _fig, axs = plt.subplots(
            1, 2, sharex=True, sharey=True, figsize=(5, 5))

        self.engagement = False
        self.keyboard = False
        self.mouse = False

        mouse_source.get_data_stream().subscribe(self.display_mouse_event)
        keyboard_source.get_data_stream().subscribe(self.display_key_event)
        engagement_source.get_data_stream().subscribe(self.display_engagement)

        self.listen(interval, history, axs)

    def listen(self, interval, history, axs):
        '''Start plotting loop'''
        length = history / interval
        points = np.zeros((length, 2))

        while 1:
            points = np.append(points, [[0, 0]], 0)[-length:]

            if self.engagement:
                points[-1, 0] = 1
                self.engagement = False
            if self.keyboard or self.mouse:
                points[-1, 1] = 1
                self.keyboard = False
                self.mouse = False

            self.plot(points[:, 0], axs[0], "Mouse & Keyboard input")
            self.plot(points[:, 1], axs[1], "Engagement")

            plt.show()
            plt.pause(interval)

    def plot(self, points, axs, title):
        '''Plot points on the axis'''
        axs.cla()
        axs.set_title(
            title + ("(present)" if points[-1] else "(absent)"), fontsize=10)
        axs.axis('off')
        axs.bar(list(len(points)), points, 1)

    def display_engagement(self, code: int):
        '''Register appropriate engagement level change'''
        self.engagement = code < 2

    def display_key_event(self):
        '''Register keyboard event'''
        self.keyboard = True

    def display_mouse_event(self):
        '''Register mouse event'''
        self.mouse = True
