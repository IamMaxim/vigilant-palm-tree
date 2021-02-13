#!/usr/bin/env python3
#
# This is the main file of the VigilantPalmTree.

from modules.video_output_window import VideoOutputWindowModule
from modules.webcam_capture import WebcamCaptureModule

if __name__ == "__main__":
    video_frame_source = WebcamCaptureModule()

    video_output = VideoOutputWindowModule(video_frame_source)

    video_frame_source.start()

    # Run UI on the MainThread
    video_output.run()
