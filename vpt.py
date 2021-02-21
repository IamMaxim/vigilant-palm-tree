#!/usr/bin/env python3
#
# This is the main file of the VigilantPalmTree.

from nodes.audio_to_file_output import AudioToFileOutputProcessor
from nodes.keyboard_capture import KeyboardCaptureProcessor
from nodes.keyboard_to_file_output import KeyboardToFileOutputProcessor
from nodes.mouse_capture import MouseCaptureProcessor
from nodes.mouse_to_file_output import MouseToFileOutputProcessor
from nodes.sound_capture import SoundCaptureProcessor
from nodes.video_output_window import VideoOutputWindowProcessor
from nodes.video_to_file_output import VideoToFileOutputProcessor
from nodes.webcam_capture import WebcamCaptureProcessor

if __name__ == "__main__":
    # Create capture nodes
    video_frame_source = WebcamCaptureProcessor()
    sound_source = SoundCaptureProcessor()
    keyboard_source = KeyboardCaptureProcessor()
    mouse_source = MouseCaptureProcessor()

    # Create GUI nodes
    gui_video_output = VideoOutputWindowProcessor(video_frame_source)

    # Create file output nodes
    video_to_file = VideoToFileOutputProcessor(video_frame_source)
    audio_to_file = AudioToFileOutputProcessor(sound_source)
    keyboard_to_file = KeyboardToFileOutputProcessor(keyboard_source)
    mouse_to_file = MouseToFileOutputProcessor(mouse_source)

    # Start capture on all types of sources
    video_frame_source.start()
    sound_source.start()
    keyboard_source.start()
    mouse_source.start()

    # Run UI on the MainThread (this is a blocking call)
    gui_video_output.run()
