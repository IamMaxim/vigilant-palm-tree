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
        fig, axs = plt.subplots(
            1, 2, sharex=True, sharey=True, figsize=(5, 3))
        fig.canvas.toolbar.pack_forget()

        n = int(history / interval)
        points = np.random.randint(0, 2, (n, 2))
        # points = np.random.zeros((n, 2))

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

            self.plot(points[:, 0], axs[0], "Input")
            self.plot(points[:, 1], axs[1], "Engagement")

            plt.xticks([0, n/2, n], [str(history)+'s',
                                     str(history / 2)+'s', str(0)+'s'])
            plt.yticks([0, 1], ['absent', 'present'])
            plt.pause(interval)

    def plot(self, points, axs, title):
        '''Plot points on the axis'''
        axs.cla()
        axs.set_title(title, fontsize=10)
        # axs.axis('off')
        axs.plot(points)

    def catch_engagement(self, code):
        '''Register appropriate engagement level change'''
        self.engagement = code < 2

    def catch_key_event(self, event):
        '''Register keyboard event'''
        input("key event")
        self.keyboard = True

    def catch_mouse_event(self, event):
        '''Register mouse event'''
        input("mouse event")
        self.mouse = True
