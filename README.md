# Vigilant Palm Tree

A research tool that allows collecting audio/video data to predict a person's state of work engagement and correlate
that data with that person's keyboard/mouse activity.

## Installation

Install the dependencies using

    pipenv install

If you are running Linux, you might need to manually install the [PortAudio](http://www.portaudio.com/) library (might
be called `libportaudio2` or similar), as well as the `libsndfile` library (called `libsndfile1` or similar). On
Windows/macOS, they are automatically installed.

On Debian/Ubuntu, you can do that using:

    sudo apt install libportaudio2 libsndfile1

On Arch Linux, use:

    sudo pacman -Sy portaudio libsndfile

## Usage

Run `pipenv run  vpt <subcommand>`. For detailed usage information, run `pipenv run vpt -h`.

If you are using Linux, you might need to run some commands as root (or with `sudo`)
as [mouse recording](https://github.com/boppreh/mouse#:~:text=requires%20sudo)
and [keyboard recording](https://github.com/boppreh/keyboard#:~:text=requires%20sudo) require it.
