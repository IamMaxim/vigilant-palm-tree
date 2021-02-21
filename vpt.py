#!/usr/bin/env python3
#
# This is the main file of the VigilantPalmTree.

from sinks.audio_to_file_output import AudioToFileOutputProcessor
from sources.keyboard_source import KeyboardSource
from sinks.keyboard_to_file_output import KeyboardToFileOutputProcessor
from sources.mouse_source import MouseSource
from sinks.mouse_to_file_output import MouseToFileOutputProcessor
from sources.sound_source import SoundSource
from sinks.video_display import VideoDisplay
from sinks.video_to_file_output import VideoToFileOutputProcessor
from sources.device_video_source import DeviceVideoSource

if __name__ == "__main__":
    # Create capture nodes
    video_source = DeviceVideoSource()
    sound_source = SoundSource()
    keyboard_source = KeyboardSource()
    mouse_source = MouseSource()

    # Create GUI nodes
    video_display = VideoDisplay(video_source)

    # Create file output nodes
    video_to_file = VideoToFileOutputProcessor(video_source)
    audio_to_file = AudioToFileOutputProcessor(sound_source)
    keyboard_to_file = KeyboardToFileOutputProcessor(keyboard_source)
    mouse_to_file = MouseToFileOutputProcessor(mouse_source)

    # Start capture on all types of sources
    video_source.start()
    sound_source.start()
    keyboard_source.start()
    mouse_source.start()

    # Run UI on the MainThread (this is a blocking call)
    video_display.run()
