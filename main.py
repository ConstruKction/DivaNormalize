import argparse
from pathlib import Path

from AudioProcessor import AudioProcessor

MODS_DIR_PATH = Path('E:/SteamLibrary/steamapps/common/Hatsune Miku Project DIVA Mega Mix Plus/mods_test')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lufs',
                        help='LUFS threshold for loudness analysis. Default is -14.',
                        type=float,
                        default=-14)
    parser.add_argument('-s', '--sample-rate',
                        help='Sample rate in Hz.',
                        type=int,
                        default=44100)
    args = parser.parse_args()

    audio_processor = AudioProcessor(MODS_DIR_PATH)
    audio_processor.load_processed_files('processed_songs.json')
    audio_processor.find_oggs()
    audio_processor.process_oggs(args.lufs, args.sample_rate)
