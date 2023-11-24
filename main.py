import argparse
from pathlib import Path

from audio_processor import AudioProcessor

MODS_DIR_PATH = Path('E:/SteamLibrary/steamapps/common/Hatsune Miku Project DIVA Mega Mix Plus/mods_test')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lufs',
                        help='LUFS threshold for loudness analysis. Default is -15.',
                        type=float,
                        default=-15)
    parser.add_argument('-s', '--sample-rate',
                        help='Sample rate in Hz. MM+ is 44100 and PDAFT is 48000.',
                        type=int,
                        default=44100)
    args = parser.parse_args()

    audio_processor = AudioProcessor(MODS_DIR_PATH)
    audio_processor.load_processed_files('processed_songs.json')
    audio_processor.find_oggs()
    audio_processor.process_oggs(args.lufs, args.sample_rate)
