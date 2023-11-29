import concurrent.futures
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List

from loguru import logger

from song_manager import SongManager
from cmd_manager import CmdManager


class Normalizer:
    def __init__(self, input_directory_path: Path, two_pass: bool):
        self.song_manager = SongManager()
        self.songs: List[Path] = self.song_manager.find_songs(input_directory_path)
        self.two_pass = two_pass

        logger.remove()
        logger.add(sys.stdout, level="INFO")

        if self.two_pass:
            logger.info('Two-pass mode enabled!')

    def process_song(self, song_path: Path, lufs: float, true_peak: float, loudness_range: float,
                     sample_rate: int) -> str:
        if song_path.name in self.song_manager.load_normalized_songs():
            logger.warning(f'{song_path.name} was normalized before -> skipping.')
            return ''

        temp_output_path = str(Path(tempfile.mkdtemp()) / song_path.name)

        cmd_manager = CmdManager()

        if self.two_pass:
            analyze_command = cmd_manager.build_analyze_command(song_path)
            analysis_data = cmd_manager.parse_song_analysis_data(cmd_manager.execute_first_pass_command(analyze_command,
                                                                                                        song_path))
            command = cmd_manager.build_normalize_command(song_path,
                                                          analysis_data['output_i'],
                                                          analysis_data['output_tp'],
                                                          analysis_data['output_lra'],
                                                          sample_rate,
                                                          temp_output_path)

            logger.info(f"{song_path.name} - "
                        f"lufs: {analysis_data['output_i']} | "
                        f"tp: {analysis_data['output_tp']} | "
                        f"lra: {analysis_data['output_lra']} | "
                        f"{sample_rate} Hz")
        else:
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
            with open('failed_songs.txt', 'w') as f:
                f.write(f'{song_path}\n')

        return normalized_song_filename

    def normalize_songs(self, lufs: float, true_peak: float, loudness_range: float, sample_rate: int) -> None:
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

        logger.success('Done.')
