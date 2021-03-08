from enum import Enum


# Wrapper around the OpenCV frame
class VideoFrame:
    def __init__(self, frame):
        self.frame = frame


# Represents an engagement state of a person
class Engagement(Enum):
    ENGAGEMENT = 1
    CONFERENCING = 2
    IDLING = 3
    DISTRACTION = 4
    ABSENCE = 5
