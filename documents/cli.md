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

To start recording the data, use the `record` option:

```
$ vpt record
```

This will start a recording session. You can minimize the command line and start working.

To stop recording, use `Ctrl+C`. Your data will be saved and you can continue recording more data at any time.

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
$ vpt record --audio AudioSource2 --video "Video source 2"
```

## Generating reports

Once you have collected some data, you may generate a PDF report with the `report` option:

```
$ vpt report
```

If you wish to only analyze a part of the data, you can specify the `--start <TIME>` and `--end <TIME>` with a time
point in the format `YYYY.MM.DD HH:MM:SS`:

```
$ vpt report --start "2021-01-01 00:00:00" --end "2021-01-07 23:59:59"
```

Omitting the `--start` will select the all the data up to `--end` and vice versa.

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

## Clearing old data

To clear the data collected by the program, use the `clear` option:

```
$ vpt clear
Warning! You are about to delete the data from 2021-01-01 13:37:00 to 2021-02-01 13:38:00.
Are you sure (y/N)?
```

Type `y` and hit `Enter` to confirm deletion.

If you only wish to delete a part of the data, you may constrain the range of deletion with `--start <TIME>`
and `--end <TIME>` options with a time point in the format `YYYY.MM.DD HH:MM:SS`:

```
$ vpt clear --start "2021-01-01 13:37:00" --end "2021-01-02 13:37:00"
Warning! You are about to delete the data from 2021-01-01 13:37:00 to 2021-01-02 13:37:00.
Are you sure (y/N)?
```










