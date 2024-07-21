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
        self.parser.add_argument('-t', '--target-level',
                                 help='Target loudness level in dB/LUFS (default: -11).',
                                 type=float,
                                 default=-11)
        self.parser.add_argument('-ar', '--sample-rate',
                                 help='Audio sample rate to use for output files in Hz. MM+ is 44100 and PDAFT is '
                                      '48000. You should change it'
                                      'depending on whether you work with AFT or MM+ files.',
                                 type=int,
                                 default=44100)

    def parse_args(self):
        return self.parser.parse_args()
