# Command-line Interface Description

The program is called `vpt`. You may launch it through your system's command line.

## Checking your configuration

To make sure your hardware is correctly functioning and recognized by the program, use the `check` option:

```
$ vpt check
```

This will record the data for 5 seconds and then create 3 files in your current working directory:

* `vpt-audio.wav`: a sample of audio recorded through your audio source

* `vpt-keyboard.txt`: a list of recorded keyboard actions

* `vpt-mouse.txt`: a list of mouse actions (moves & clicks)

Feel free to use your keyboard and mouse during the 5 seconds of the check to ensure that the data from them is
correctly recorded.

You may pass the `--audio` and `--video` parameters to pick specific devices to be used for recordings. The system
defaults will be used if omitted. Additionally, you may use the `--duration` option to customize the recording
duration (in seconds).

## Data collection

To launch the application, simply launch the executable without any parameters:

```
$ vpt
```

This will open a window with live graphs of data and buttons to start/stop recording. You may minimize the

If the recording process unexpectedly terminates, the data will still be saved.

## Configuring inputs

If you have multiple audio/video sources, you can select between them.

To list all available sources, use the `sources` option with the type (`audio` or `video`):

```
$ vpt sources audio
AudioSource1
AudioSource2
AudioSource3
$ vpt sources video
Video source 1
Video source 2
```

To select an audio source for recording, use `--audio <NAME>` for specifying the audio source and `--video <NAME>` for
specifying the video source:

```
$ vpt --audio AudioSource2 --video "Video source 2"
```


## Obtaining raw data for analysis

If you wish to get a dataset of keyboard/mouse activity along with the predicted work state engagement levels from
audio/video, use the `dump` option:

```
$ vpt dump
```

This will create a `vpt-data.sql` SQLite database in the current working directory with the collected data.

To dump the data into a different file, use the `-o` parameter:

```
$ vpt dump -o for-analysis.sql
```
