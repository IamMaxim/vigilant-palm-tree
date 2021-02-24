'''Manages obtaining the available input/output sources.'''
from textwrap import shorten
from typing import List

import cv2
import sounddevice as sd


def get_default_audio_input_name() -> str:
    '''Gets the name of the default audio input device.'''
    return sd.query_devices(kind='input')['name']


def list_audio_inputs() -> List[dict]:
    '''Returns a list of all audio input devices.'''
    devices = sd.query_devices()
    default = sd.query_devices(kind='input')
    devices = [device for device in devices if device['max_input_channels'] > 0]
    for device in devices:
        if device == default:
            device['default'] = True
        else:
            device['default'] = False
    return devices


def print_audio_inputs():
    '''Prints the available input devices in a nice table.'''
    devices = list_audio_inputs()
    print(f'┌{"-" * 52}┬{"-" * 12}┬{"-" * 14}┐')
    print(f'| {"Name":^50} | {"Channels":^10} | {"Sample rate":^12} |')
    print(f'├{"-" * 52}┼{"-" * 12}┼{"-" * 14}┤')
    for device in devices:
        if device['default']:
            device['name'] = '* ' + device['name']
        device['name'] = shorten(device['name'], width=50, placeholder='..')
        print(f'| {device["name"]:<50} | {device["max_input_channels"]:^10} '
              f'| {device["default_samplerate"]:^12} |')
    print(f'└{"-" * 52}┴{"-" * 12}┴{"-" * 14}┘')
    print('* = default')


def list_video_inputs():
    """Returns a list of all video input devices (a.k.a. cameras)"""
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        arr.append(index)
        cap.release()
        index += 1
    return arr


def print_video_inputs():
    """Prints the list of available cameras neatly."""
    print(list_video_inputs())
