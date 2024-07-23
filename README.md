# Diva Normalize

This simple command-line tool helps you normalize audio volumes in your mods directory by applying dual-pass Loudness Units Full
Scale (LUFS) normalization. It utilizes slhck's [ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) for audio processing and operates in a multithreaded manner.
It's made to use 100% of your CPU until it's finished.

## Usage
```bash
python main.py -i "/path/to/your/mods"
```
```bash
python main.py -i "/path/to/your/mods" -t -15 -ar 48000
```

## Arguments
- `-h`, `--help`: Show the help message and exit.
- `-i INPUT`, `--input INPUT`: Full path to a directory containing audio files. All folders will be scanned recursively for 'song' folders with *.ogg files inside. Default is the current directory.
- `-t TARGET_LEVEL`, `--target-level TARGET_LEVEL`: Target loudness level in LUFS. Default is -11 dB LUFS.
- `-ar SAMPLE_RATE`, `--sample-rate SAMPLE_RATE`: Sample rate in Hz. MM+ is 44100 Hz and PDAFT is 48000 Hz. Default is 44100 Hz.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ConstruKction/DivaNormalize.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install FFmpeg using your package manager or download the most recent version from [here](https://www.ffmpeg.org/download.html).
4. *WINDOWS ONLY*: You must add FFmpeg to the [PATH environment variable](https://superuser.com/a/284351).

## How It Works

The program reads audio files (.ogg format) within the specified mods directory and normalizes their volumes according to
the provided LUFS threshold. The processing is multithreaded, and it WILL load your CPU to 100%. The processed files are
then overwritten in place.

## Benchmark

On a Ryzen 3600, normalizing approximately 700 songs took around 48 minutes at full CPU load.

## Disclaimer

I am not responsible for *ANY* corrupt song files, damaged mods, or unintended consequences to your Diva
installation. This tool operates on any directory given directly and **overwrites** files, so it's always a good idea to back up your mods before using
this script. Playtest a variety of songs to ensure you're satisfied with the selected LUFS threshold (especially if
different from the default) before committing to any irreversible changes.

## Dependencies

- [FFmpeg](https://ffmpeg.org/): Required for audio processing.
- [ffmpeg-normalize](https://pypi.org/project/ffmpeg-normalize/): For much easier dual-pass capabilities.
- [loguru](https://pypi.org/project/loguru/): Used for logging information.
- [humanize](https://pypi.org/project/humanize/): Used for turning numbers into fuzzy human-readable duration.

## Notes

- The tool maintains a list of processed songs in the `processed_songs.txt` file to skip duplicates during subsequent
  runs.

Feel free to fork & customize the script according to your needs.
