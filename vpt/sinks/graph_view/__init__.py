"""Display graphs & app controls."""

import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np

from rx import operators

from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase


class GraphView(SinkBase):
    """A sink node to display the graphs."""

    def __init__(self, mouse_source: SourceBase,
                 keyboard_source: SourceBase,
                 engagement_source: SourceBase):
        """Add periodically redrawing canvas to TkWindow"""
        print('__init__')

        # self.engagement = False
        # self.keyboard = False
        # self.mouse = False

        self.last_keyboard_time = 0
        self.last_mouse_time = 0

        self.history = 5

        self.points = np.empty((0, 2))

        print('creating subplots')
        # fig, self.axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(5, 2))
        fig, self.axs = plt.subplots(1, 2, figsize=(5, 2))
        print('created')
        # fig.canvas.toolbar.pack_forget()

        # mouse_source.get_data_stream().subscribe(self.catch_mouse_event)
        # keyboard_source.get_data_stream().subscribe(self.catch_key_event)
        # engagement_source.get_data_stream().subscribe(self.catch_engagement)

        print('subscribing')
        mouse_source.get_data_stream().pipe(operators.combine_latest(
            keyboard_source.get_data_stream(),
            engagement_source.get_data_stream()
        )).subscribe(self.update_data)

    def update_data(self, data):
        print('updating data')
        self.data = data

    def update(self):
        print('update')
        try:
            mouse, keyboard, engagement = self.data
            print('got data')

            kb_event = self.last_keyboard_time != keyboard.time
            ms_event = self.last_mouse_time != mouse.time

            if kb_event:
                self.last_keyboard_time = keyboard.time

            if ms_event:
                self.last_mouse_time = mouse.time

            # self.points = np.append(np.array([kb_event or ms_event, engagement]), self.points)

            print('concating')
            self.points = np.concatenate((np.array([kb_event or ms_event, engagement]).reshape(1, 2), self.points),
                                         axis=0)
            print('concated')

            # self.points = np.append(self.points, np.random.randint(0, 2, (1, 2)), 0)[-n:]
            # points = np.append(points, [[0, 0]], 0)[-n:]

            # if self.engagement:
            #     points[-1, 0] = 1
            #     self.engagement = False
            # if self.keyboard or self.mouse:
            #     points[-1, 1] = 1
            #     self.keyboard = False
            #     self.mouse = False

            print('plotting')
            self.plot(self.points[:, 0], self.axs[0], "Input (mouse/keyboard)")
            self.plot(self.points[:, 1], self.axs[1], "Engagement")
            print('plotted')

            # plt.xticks([0, len(self.points) / 2, len(self.points)], [str(self.history) + 's',
            #                                                          str(self.history / 2) + 's', str(0) + 's'])
            # plt.yticks([0.1, 1.1], ['absent', 'present'])
            # plt.ion()
            # plt.show()
            # plt.pause(0.001)
        except AttributeError:
            # No data yet
            pass

    def plot(self, points, axs, title):
        """Plot points on the axis"""
        axs.cla()
        axs.set_title(title, fontsize=10)
        axs.bar(range(points.shape[0]), points + 0.1)

    # def catch_engagement(self, value):
    #     """Register appropriate engagement level change"""
    #     self.engagement = value > 0.5
    #
    # def catch_key_event(self, event):
    #     """Register keyboard event"""
    #     input("key event")
    #     self.keyboard = True
    #
    # def catch_mouse_event(self, event):
    #     '''Register mouse event'''
    #     input("mouse event")
    #     self.mouse = True
