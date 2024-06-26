# Diva Normalize

This simple command-line tool helps you normalize audio volumes in your mods directory by applying Loudness Units Full
Scale (LUFS) normalization. It utilizes the FFmpeg library for audio processing and operates in a multithreaded manner.
It's made to use 100% of your CPU until it's finished.

## Usage
```bash
python main.py -i /path/to/your/mods
```
```bash
python main.py -i /path/to/your/mods -l -16 -p -2 -r 10 -s 44100
```

## Arguments
- `-h`, `--help`: Show the help message and exit.
- `-i INPUT`, `--input INPUT`: Full path to a directory containing audio files. All folders will be scanned recursively for 'song' folders with *.ogg files inside. Default is the current directory.
- `-l LUFS`, `--lufs LUFS`: Target loudness level in dB LUFS. Default is -15 dB LUFS.
- `-p TRUE_PEAK`, `--true-peak TRUE_PEAK`: Target True Peak level in dBFS. Default is -1 dBFS.
- `-r LOUDNESS_RANGE`, `--loudness-range LOUDNESS_RANGE`: Loudness range, controlling the amount of gain applied to the audio. Default is 11 LU.
- `-s SAMPLE_RATE`, `--sample-rate SAMPLE_RATE`: Sample rate in Hz. MM+ is 44100 and PDAFT is 48000. Change depending on the audio file format. Default is 44100.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ConstruKction/DivaNormalize.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## How It Works

The program reads audio files (OGG format) within the specified mods directory and normalizes their volumes according to
the provided LUFS threshold. The processing is multithreaded, and it WILL load your CPU to 100%. The processed files are
then overwritten in place.

## Benchmark

On a Ryzen 3600, normalizing approximately 500 songs took around 20 minutes at full CPU load.

## Disclaimer

I am not responsible for any corrupt song files, damaged mods, or unintended consequences to your entire Diva
installation. This tool operates on your mods directory, and it's always a good idea to back up your mods before using
this script. Playtest a variety of songs to ensure you're satisfied with the selected LUFS threshold (especially if
different from the default) before committing to any irreversible changes.

## Dependencies

- [FFmpeg](https://ffmpeg.org/): Required for audio processing.
- [loguru](https://pypi.org/project/loguru/): Used for logging information.

## Notes

- The tool maintains a list of processed songs in the `processed_songs.txt` file to skip duplicates during subsequent
  runs.

Feel free to customize the script according to your needs.
