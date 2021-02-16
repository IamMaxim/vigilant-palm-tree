# Vigilant Palm Tree

A research tool that allows collecting audio/video data to predict a person's state of work engagement and correlate that data with that person's keyboard/mouse activity. 

## Installation

Install the requirements using `pip install -r requirements.txt`. 
_Note: depending on your platform, you might need to use `pip3` instead of `pip`._

If you are running Linux, you might need to manually install the [PortAudio](http://www.portaudio.com/) library (might be called `libportaudio2` or similar), as well as the `libsndfile` library (called `libsndfile1` or similar).
On Windows/macOS, they are automatically installed.

## Usage

Run `python -m vpt <subcommand>`. For detailed usage information, run `python vpt -h`.
_Note: depending on your platform, you might need to use `python3` instead of `python`._

If you are using Linux, you might need to run some commands as root (or with `sudo`) as [mouse recording](https://github.com/boppreh/mouse#:~:text=requires%20sudo) and [keyboard recording](https://github.com/boppreh/keyboard#:~:text=requires%20sudo) require it.
