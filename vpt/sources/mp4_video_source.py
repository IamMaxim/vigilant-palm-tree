'''Gets the video from an MP4 file.'''

import threading

import cv2
from rx import Observable
from rx.subject import Subject
from rx.scheduler.mainloop import QtScheduler

from vpt.data_structures import VideoFrame
from vpt.sources.base import SourceBase


class MP4VideoSource(SourceBase[VideoFrame]):
    '''A data source for the video stream from an MP4 file.'''
    _subj: Subject
    _thread: threading.Thread

    def __init__(self, filename: str):
        self._subj = Subject()
        self.stopped = True

        self.video_capture = cv2.VideoCapture(filename)
        if not self.video_capture.isOpened():
            raise ValueError('could not open video stream for file {}'.format(filename))

    def start(self, _scheduler: QtScheduler):
        '''Start the capturing thread.'''
        if not self.stopped:
            return
        self.stopped = False
        self._thread = threading.Thread(target=self.run_threaded)
        self._thread.start()

    def stop(self):
        '''Stop the capturing thread.'''
        if self.stopped:
            return
        self.stopped = True
        self._thread.join()

    def run_threaded(self):
        '''The main loop fetching frames from a file.'''
        while not self.stopped:
            ret, frame = self.video_capture.read()

            if not ret:
                break

            self._subj.on_next(VideoFrame(frame))

    @property
    def output(self) -> Observable:
        '''Getter for the video frames observable.'''
        return self._subj
