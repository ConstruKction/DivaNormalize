import concurrent.futures
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import List

from loguru import logger

from song_manager import SongManager
from cmd_manager import CmdManager


class Normalizer:
    def __init__(self, input_directory_path: Path):
        self.song_manager = SongManager()
        self.songs: List[Path] = self.song_manager.find_songs(input_directory_path)
        self.initialize_processed_songs_file()

        logger.remove()
        logger.add(sys.stdout, level="INFO")

    @staticmethod
    def initialize_processed_songs_file():
        processed_songs_file = Path('processed_songs.txt')
        if not processed_songs_file.exists():
            processed_songs_file.touch()

    @staticmethod
    def verify_range(number: float, min_range: float, max_range: float, name: str) -> float:
        n = float(number)
        if n < min_range or n > max_range:
            logger.warning(f'{name} must be within {min_range} and {max_range}.')

        if n < min_range:
            logger.warning(f'Adjusting {name} from {number} to {min_range}.')
            return min_range
        elif n > max_range:
            logger.warning(f'Adjusting {name} from {number} to {max_range}.')
            return max_range
        else:
            return number

    def process_song(self, song_path: Path, lufs: float, true_peak: float, loudness_range: float,
                     sample_rate: int) -> str:
        if song_path.name in self.song_manager.load_normalized_songs():
            logger.warning(f'{song_path.name} was normalized before -> skipping.')
            return ''

        temp_output_path = str(Path(tempfile.mkdtemp()) / song_path.name)

        cmd_manager = CmdManager()

        command = cmd_manager.build_normalize_command(song_path,
                                                      lufs,
                                                      true_peak,
                                                      loudness_range,
                                                      sample_rate,
                                                      temp_output_path)

        normalized_song_filename = cmd_manager.execute_normalize_command(command, song_path)

        if Path(temp_output_path).exists():
            shutil.move(temp_output_path, song_path)  # Rename the temp file to overwrite the original
            logger.success(f'{song_path.name} normalized!')
        else:
            logger.error(f'Temp file not found for {song_path.name}. Skipped & saved in failed_songs.txt.')
            with open('failed_songs.txt', 'a') as f:
                f.write(f'{song_path}\n')

        return normalized_song_filename

    def normalize_songs(self, lufs: float, true_peak: float, loudness_range: float, sample_rate: int) -> None:
        start_time = time.time()

        normalized_songs = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.process_song, song, lufs, true_peak, loudness_range, sample_rate) for song
                       in self.songs]

            for future in concurrent.futures.as_completed(futures):
                try:
                    normalized_song = future.result()
                    if not normalized_song:
                        # Skip normalizing if the result is empty (indicating an error)
                        continue
                except Exception as e:
                    logger.error(f'An error occurred in process: {e}')
                else:
                    normalized_songs.append(normalized_song)

            self.song_manager.update_normalized_songs_file(normalized_songs)

        end_time = time.time()
        elapsed_time_seconds = end_time - start_time
        elapsed_time_minutes = elapsed_time_seconds / 60.0
        logger.success(f'Done! Finished in {elapsed_time_minutes:.2f} minutes.')
