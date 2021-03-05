"""Display graphs & app controls."""
import time

import keyboard
import matplotlib
import mouse

from data_structures import VideoFrame
import matplotlib.pyplot as plt
import numpy as np

from rx import operators

from vpt.sinks.base import SinkBase
from vpt.sources.base import SourceBase

matplotlib.use("Qt5Agg")


class GraphView(SinkBase):
    """A sink node to display the graphs."""

    def __init__(self,
                 video_source: SourceBase[VideoFrame],
                 mouse_source: SourceBase,
                 keyboard_source: SourceBase,
                 engagement_source: SourceBase):
        self.last_keyboard_time = 0
        self.last_mouse_time = 0

        self.max_points = 32

        self.points = np.empty((0, 2))

        fig, self.axs = plt.subplots(2, 2, figsize=(5, 2))

        initial_keyboard_event = keyboard.KeyboardEvent(keyboard.KEY_UP, 0)
        initial_mouse_event = mouse.ButtonEvent(event_type=mouse.UP, button=0, time=time.time())

        mouse_source.get_data_stream() \
            .pipe(operators.start_with(initial_mouse_event)) \
            .pipe(operators.combine_latest(
            video_source.get_data_stream().pipe(operators.start_with(None)),
            keyboard_source.get_data_stream().pipe(operators.start_with(initial_keyboard_event)),
            engagement_source.get_data_stream()
        )).subscribe(self.update_data)

    def update_data(self, data):
        self.data = data

    def update(self):
        try:
            mouse, frame, keyboard, engagement = self.data

            kb_event = self.last_keyboard_time != keyboard.time
            ms_event = self.last_mouse_time != mouse.time

            if kb_event:
                self.last_keyboard_time = keyboard.time

            if ms_event:
                self.last_mouse_time = mouse.time

            self.points = np.concatenate((self.points, np.array([kb_event or ms_event, engagement]).reshape(1, 2)),
                                         axis=0)

            # Truncate the data to self.max_points latest values
            if self.points.shape[0] > self.max_points:
                self.points = self.points[self.points.shape[0] - self.max_points: self.points.shape[0], :]

            print('plotting')
            if frame is not None:
                plt.subplot(2, 2, 1)
                plt.imshow(frame.frame)
            self.plot(self.points[:, 0], self.axs[1][0], "Input (mouse/keyboard)")
            self.plot(self.points[:, 1], self.axs[1][1], "Engagement")
            print('plotted')

            plt.ion()
            plt.pause(0.016)
        except AttributeError:
            # No data yet
            pass

    def plot(self, points, axs, title):
        """Plot points on the axis"""
        axs.cla()
        axs.set_title(title, fontsize=10)
        axs.bar(range(points.shape[0]), points + 0.1)
