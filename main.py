import argparse
from pathlib import Path

from audio_processor import AudioProcessor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        help='FULL PATH to your mods directory. Default is wherever the script is.',
                        type=Path,
                        default='.')
    parser.add_argument('-l', '--lufs',
                        help='Target loudness level. Default is -15 dB LUFS.',
                        type=float,
                        default=-15)
    parser.add_argument('-p', '--true-peak',
                        help='Target True Peak level. Default is -1.5 dBFS.',
                        type=float,
                        default=-1.5)
    parser.add_argument('-r', '--loudness-range',
                        help='Loudness range, i.e. controls the amount of gain applied to the audio. Default is 11 LU.',
                        type=float,
                        default=11)
    parser.add_argument('-s', '--sample-rate',
                        help='Sample rate in Hz. MM+ is 44100 and PDAFT is 48000.',
                        type=int,
                        default=44100)
    args = parser.parse_args()

    audio_processor = AudioProcessor(args.input)
    audio_processor.find_oggs()
    audio_processor.process_oggs(args.lufs, args.true_peak, args.loudness_range,args.sample_rate)


if __name__ == '__main__':
    main()
