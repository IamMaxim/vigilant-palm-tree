# Command-line Interface Description

The program is called `vpt`. You may launch it through your system's command line.

## Checking your configuration

To make sure your hardware is correctly functioning and recognized by the program, use the `check` option:

```sh
vpt check
```

This will record the data for 5 seconds and then create 3 files in your current working directory:

- `vpt-audio.wav`: a sample of audio recorded through your audio source

- `vpt-keyboard.txt`: a list of recorded keyboard actions

- `vpt-mouse.txt`: a list of mouse actions (moves & clicks)

Feel free to use your keyboard and mouse during the 5 seconds of the check to ensure that the data from them is
correctly recorded.

You may pass the `--audio` and `--video` parameters to pick specific devices to be used for recordings. The system
defaults will be used if omitted. Additionally, you may use the `--duration` option to customize the recording
duration (in seconds).

## Data collection

To launch the application, simply start the executable without any parameters:

```sh
vpt
```

This will open a window with live graphs of data and buttons to start/stop recording. You may minimize the window and start working now.

If the recording process unexpectedly terminates, the data will still be saved.

## Configuring inputs

If you have multiple audio/video sources, you can select between them.

To list all available sources, use the `sources` option with the type (`audio` or `video`):

```sh
$ vpt sources audio
ID  Name
 1   AudioSource1
 2   AudioSource2
 3   AudioSource3
$ vpt sources video
Video source 1
Video source 2
```

To select an audio source for recording, use `--audio <ID>` for specifying the audio source and `--video <NAME>` for
specifying the video source:

```sh
vpt --audio 3 --video "Video source 2"
```

## Obtaining raw data for analysis

If you wish to get a dataset of keyboard/mouse activity along with the predicted work state engagement levels from
audio/video, use the `dump` option:

```sh
vpt dump
```

This will create a `vpt-data.sql` SQLite database in the current working directory with the collected data.

To dump the data into a different file, use the `-o` parameter:

```sh
$ vpt dump -o for-analysis.sql
```

## Clearing old data

To clear the data collected by the program, use the `clear` option:

```sh
$ vpt clear
Warning! You are about to delete the data from 2021-01-01 13:37:00 to 2021-02-01 13:38:00.
Are you sure (y/N)?
```

Type `y` and hit `Enter` to confirm deletion.

If you only wish to delete a part of the data, you may constrain the range of deletion with `--start <TIME>`
and `--end <TIME>` options with a time point in the format `YYYY.MM.DD HH:MM:SS`:

```sh
$ vpt clear --start "2021-01-01 13:37:00" --end "2021-01-02 13:37:00"
Warning! You are about to delete the data from 2021-01-01 13:37:00 to 2021-01-02 13:37:00.
Are you sure (y/N)?
```
