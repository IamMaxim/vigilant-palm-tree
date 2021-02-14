'''A group of functions to make sure the hardware is correctly functioning
    and recognized by the program.'''
import sounddevice as sd
import soundfile as sf

def record_audio(device=None, duration=5, filename='vpt-audio.wav'):
    '''Records audio from the given device and saves it to disk.
       Note that it currently blocks the main thread for the given duration.'''
    if device is None:
        device = sd.query_devices(kind='input')
    else:
        device = sd.query_devices(device)

    samplerate = int(device['default_samplerate'])
    channels = min(2, device['max_input_channels'])

    sd.default.samplerate = samplerate
    sd.default.channels = channels

    data = sd.rec(int(samplerate * duration))
    sd.wait()
    with sf.SoundFile(filename, mode='w', samplerate=samplerate, channels=channels) as file:
        file.write(data)
