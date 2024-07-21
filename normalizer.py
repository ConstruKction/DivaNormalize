import concurrent.futures
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import List

from humanize.time import precisedelta
from loguru import logger

from command_manager import CommandManager
from song_manager import SongManager


class Normalizer:
    def __init__(self, input_directory_path: Path):
        self.song_manager = SongManager()
        self.songs: List[Path] = self.song_manager.find_songs(input_directory_path)

        logger.remove()
        logger.add(sys.stdout, level="INFO")

    @staticmethod
    def verify_range(number: float, min_range: float, max_range: float, option_name: str) -> float:
        if number > 0:
            logger.warning(f"{option_name} must be a negative number. Reverting to default (-11).")
            return -11

        n = float(number)
        if n < min_range or n > max_range:
            logger.warning(f'{option_name} must be within {min_range} and {max_range}.')

        if n < min_range:
            logger.warning(f'Adjusting wrong {option_name} from {number} to {min_range}.')
            return min_range
        elif n > max_range:
            logger.warning(f'Adjusting wrong {option_name} from {number} to {max_range}.')
            return max_range
        else:
            return number

    @staticmethod
    def verify_sample_rate(value: int) -> int:
        if value in {44100, 48000}:
            return value

        diff_44100 = abs(value - 44100)
        diff_48000 = abs(value - 48000)

        if diff_44100 < diff_48000:
            logger.warning(f"Adjusting wrong sample rate of {value} Hz to 44100 Hz.")
            return 44100
        else:
            logger.warning(f"Adjusting wrong sample rate of {value} Hz to 48000 Hz.")
            return 48000

    @staticmethod
    def calculate_elapsed_time(start_time: float) -> str:
        end_time = time.time()
        elapsed_time_seconds = end_time - start_time
        return precisedelta(int(elapsed_time_seconds), format='%0.0f')

    def process_song(self, song_path: Path, target_level: float, sample_rate: int) -> str:
        if song_path.name in self.song_manager.load_normalized_songs():
            logger.info(f'{song_path.name} was normalized before -> skipping.')
            return ''

        temp_output_path = Path(tempfile.mkdtemp()) / song_path.name

        cmd_manager = CommandManager()
        command = cmd_manager.build_normalize_command(song_path,
                                                      target_level,
                                                      sample_rate,
                                                      f"{temp_output_path}")

        normalized_song_filename = cmd_manager.execute_normalize_command(command, song_path)

        if Path(temp_output_path).exists():
            shutil.move(temp_output_path, song_path)  # Rename the temp file to overwrite the original
            logger.success(f'{song_path.name} normalized!')
        else:
            logger.error(f'Temp file not found for {song_path.name}. Skipped & saved in failed_songs.txt.')
            with open('failed_songs.txt', 'a+') as f:
                f.write(f'{song_path}\n')

        return normalized_song_filename

    def normalize_songs(self, target_level: float, sample_rate: int):
        start_time = time.time()

        verified_target_level = self.verify_range(target_level, -70.0, -5.0, 'Target Level')
        verified_sample_rate = self.verify_sample_rate(sample_rate)

        Path.touch(Path("processed_songs.txt"))

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.process_song, song, verified_target_level, verified_sample_rate) for song
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
                    self.song_manager.update_normalized_songs_file(normalized_song)

        logger.success(f"Done! Finished in {self.calculate_elapsed_time(start_time)}.")
