import concurrent.futures
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List

from loguru import logger

from song_manager import SongManager
from cmd_parser import CmdParser


class Normalizer:
    def __init__(self, input_directory_path: Path):
        self.song_manager = SongManager()
        self.songs: List[Path] = self.song_manager.find_songs(input_directory_path)

        logger.remove()
        logger.add(sys.stdout, level="INFO")

    def process_song(self, ogg: Path, lufs: float, true_peak: float, loudness_range: float, sample_rate: int) -> str:
        if ogg.name in self.song_manager.load_normalized_songs():
            logger.warning(f'{ogg.name} was normalized before -> skipping.')
            return ''

        temp_output_path = str(Path(tempfile.mkdtemp()) / ogg.name)

        cmd_parser = CmdParser()
        command = cmd_parser.build_command(ogg, lufs, true_peak, loudness_range, sample_rate, temp_output_path)
        processed_ogg_filename = cmd_parser.execute_command(command, ogg)

        shutil.move(temp_output_path, ogg)  # Rename the temp file to overwrite the original

        logger.success(f'{ogg.name} normalized!')

        return processed_ogg_filename

    def normalize_songs(self, lufs: float, true_peak: float, loudness_range: float, sample_rate: int) -> None:
        normalized_songs = []

        logger.info(f'Target Loudness: {lufs} dB LUFS')
        logger.info(f'True Peak: {true_peak} dBFS')
        logger.info(f'Loudness Range: {loudness_range} LU')
        logger.info(f'Sample Rate: {sample_rate} Hz')

        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Use executor.map to parallelize the processing of oggs
            normalized_songs_task_output = executor.map(self.process_song,
                                                        self.songs,
                                                        [lufs] * len(self.songs),
                                                        [true_peak] * len(self.songs),
                                                        [loudness_range] * len(self.songs),
                                                        [sample_rate] * len(self.songs))

            for normalized_song in normalized_songs_task_output:
                normalized_songs.append(normalized_song)

            self.song_manager.update_normalized_songs_file(normalized_songs)

        logger.success('Done.')
