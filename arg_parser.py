import argparse
from pathlib import Path


class ArgParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-i', '--input',
                                 help='Full path to a directory. Default is wherever the script is. All folders will '
                                      'be scanned recursively for \'song\' folders with *.ogg files inside.',
                                 type=Path,
                                 default='.')
        self.parser.add_argument('-l', '--lufs',
                                 help='Target loudness level. Default is -14 dB LUFS.',
                                 type=float,
                                 default=-14)
        self.parser.add_argument('-p', '--true-peak',
                                 help='Target True Peak level. Default is -1 dBFS.',
                                 type=float,
                                 default=-1)
        self.parser.add_argument('-r', '--loudness-range',
                                 help='Loudness range, i.e. controls the amount of gain applied to the audio. Default '
                                      'is 11 LU.',
                                 type=float,
                                 default=11)
        self.parser.add_argument('-s', '--sample-rate',
                                 help='Sample rate in Hz. MM+ is 44100 and PDAFT is 48000. You should change it '
                                      'depending on whether you work with AFT files or MM+ files.',
                                 type=int,
                                 default=44100)

    def parse_args(self):
        return self.parser.parse_args()
