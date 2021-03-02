"""The module responsible for estimating the engagement of the user."""
import time

import keyboard
import mouse
import numpy as np
from rx import Observable, operators
from rx.subject import Subject

from vpt.processors.base import ProcessorBase
from vpt.sources.base import SourceBase


class EngagementEstimator(ProcessorBase):
    """Given gaze and speech data, estimates the user's engagement level."""

    def __init__(self, head_rotation_vector: SourceBase[np.ndarray], voice_present: SourceBase[bool],
                 keyboard_source: SourceBase, mouse_source: SourceBase):
        self.subj = Subject()

        # Current state
        self.rotation_accum = 0
        self.voice_accum = 0
        self.keyboard_accum = 0
        self.mouse_accum = 0

        self.last_kb_event = 0
        self.last_ms_event = 0

        # Initial events for keyboard and mouse are required as video/audio is a continuous stream of data, but keyboard
        # or mouse events may not be generated for a long time initially. Until each of input observables have at least
        # one object, the final outputting object is not emitted.
        initial_keyboard_event = keyboard.KeyboardEvent(keyboard.KEY_UP, 0)
        initial_mouse_event = mouse.ButtonEvent(event_type=mouse.UP, button=0, time=time.time())

        # Observable with all data channels merged into one stream
        obs = head_rotation_vector.get_data_stream().pipe(operators.combine_latest(
            voice_present.get_data_stream(),
            keyboard_source.get_data_stream().pipe(operators.start_with(initial_keyboard_event)),
            mouse_source.get_data_stream().pipe(operators.start_with(initial_mouse_event))
        ))

        obs.subscribe(self.process_state)

    def process_state(self, state):
        rot, voice, kb, ms = state

        # self.rotation_accum += (rotation_boundary - np.linalg.norm(rot)) * 0.01 / (self.rotation_accum + 1)
        self.rotation_accum = 1 - np.linalg.norm(rot)
        self.voice_accum += ((int(voice)) - 0.5) * 0.01

        self.voice_accum = max(min(0.1, self.voice_accum), -0.1)

        if self.last_kb_event != kb.time:
            self.last_kb_event = kb.time
            self.keyboard_accum = 0

        if self.last_ms_event != ms.time:
            self.last_ms_event = ms.time
            self.mouse_accum = 0

        self.keyboard_accum += 1 / (kb.time - time.time() + 10) * 0.01
        self.mouse_accum += 1 / (ms.time - time.time() + 10) * 0.01

        self.keyboard_accum = max(min(0.1, self.keyboard_accum), -0.1)
        self.mouse_accum = max(min(0.1, self.mouse_accum), -0.1)

        res = self.rotation_accum + self.voice_accum + self.keyboard_accum + self.mouse_accum

        # print(voice, self.rotation_accum, self.voice_accum, self.keyboard_accum, self.mouse_accum)

        self.subj.on_next(res)

    def get_data_stream(self) -> Observable:
        return self.subj

    def start(self):
        pass

    def stop(self):
        pass
