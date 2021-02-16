#!/usr/bin/env python3
#
# This is the main file of the VigilantPalmTree.
import keyboard
import mouse

from modules.keyboard_capture import KeyboardCaptureModule
from modules.mouse_capture import MouseCaptureModule
from modules.sound_capture import SoundCaptureModule
from modules.video_output_window import VideoOutputWindowModule
from modules.video_to_file_output import VideoToFileOutputModule
from modules.webcam_capture import WebcamCaptureModule

if __name__ == "__main__":
    video_frame_source = WebcamCaptureModule()
    sound_source = SoundCaptureModule()
    keyboard_source = KeyboardCaptureModule()
    mouse_source = MouseCaptureModule()


    def sound_callback(rec):
        print(rec)


    def keyboard_callback(event: keyboard.KeyboardEvent):
        print('%s pressed' % event.name)


    def mouse_callback(event: mouse.MoveEvent):
        print('mouse moved to %i %i' % (event.x, event.y))


    sound_source.get_data_stream().subscribe(sound_callback)
    keyboard_source.get_data_stream().subscribe(keyboard_callback)
    mouse_source.get_data_stream().subscribe(mouse_callback)

    video_output = VideoOutputWindowModule(video_frame_source)

    video_to_file = VideoToFileOutputModule(video_frame_source)

    video_frame_source.start()
    sound_source.start()
    keyboard_source.start()
    mouse_source.start()

    # Run UI on the MainThread
    video_output.run()
