"""Display graphs & app controls."""
import time

import keyboard
import matplotlib
import mouse

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
        self.last_keyboard_time = 0
        self.last_mouse_time = 0

        self.max_points = 32

        self.points = np.empty((0, 2))

        fig, self.axs = plt.subplots(1, 2, figsize=(5, 2))

        initial_keyboard_event = keyboard.KeyboardEvent(keyboard.KEY_UP, 0)
        initial_mouse_event = mouse.ButtonEvent(event_type=mouse.UP, button=0, time=time.time())

        mouse_source.get_data_stream() \
            .pipe(operators.start_with(initial_mouse_event)) \
            .pipe(operators.combine_latest(
            keyboard_source.get_data_stream().pipe(operators.start_with(initial_keyboard_event)),
            engagement_source.get_data_stream()
        )).subscribe(self.update_data)

    def update_data(self, data):
        self.data = data

    def update(self):
        try:
            mouse, keyboard, engagement = self.data

            kb_event = self.last_keyboard_time != keyboard.time
            ms_event = self.last_mouse_time != mouse.time

            if kb_event:
                self.last_keyboard_time = keyboard.time

            if ms_event:
                self.last_mouse_time = mouse.time

            # self.points = np.append(np.array([kb_event or ms_event, engagement]), self.points)

            self.points = np.concatenate((self.points, np.array([kb_event or ms_event, engagement]).reshape(1, 2)),
                                         axis=0)

            # Truncate the data to self.max_points latest values
            if self.points.shape[0] > self.max_points:
                self.points = self.points[self.points.shape[0] - self.max_points: self.points.shape[0], :]

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

            plt.ion()
            plt.pause(0.001)
        except AttributeError:
            # No data yet
            pass

    def plot(self, points, axs, title):
        """Plot points on the axis"""
        axs.cla()
        axs.set_title(title, fontsize=10)
        axs.bar(range(points.shape[0]), points + 0.1)
