import concurrent.futures
import shutil
import sys
import tempfile
from pathlib import Path
from typing import List

from loguru import logger

from song_manager import SongManager
from cmd_parser import CmdParser


class AudioProcessor:
    def __init__(self, mods_dir_path: Path):
        self.mods_dir_path = mods_dir_path
        self.oggs: List[Path] = []
        self.processed_oggs: List[str] = []
        self.song_manager = SongManager()
        self.cmd_parser = CmdParser()

        logger.remove()
        logger.add(sys.stdout, level="INFO")

    def find_oggs(self) -> None:
        if not self.mods_dir_path.exists():
            logger.critical('Invalid mod directory path.')
            sys.exit(1)

        for path in Path(self.mods_dir_path).rglob('song/*.ogg'):
            self.oggs.append(path)

    def process_ogg(self, ogg: Path, lufs: float, true_peak: float, loudness_range: float, sample_rate: int) -> str:
        if ogg.name in self.song_manager.load_normalized_oggs():
            logger.warning(f'{ogg.name} was normalized before -> skipping.')
            return ''

        temp_output_path = str(Path(tempfile.mkdtemp()) / ogg.name)

        command = self.cmd_parser.build_command(ogg, lufs, true_peak, loudness_range, sample_rate, temp_output_path)
        processed_ogg_filename = self.cmd_parser.execute_command(command, ogg)

        shutil.move(temp_output_path, ogg)  # Rename the temp file to overwrite the original

        logger.success(f'{ogg.name} normalized!')

        return processed_ogg_filename

    def process_oggs(self, lufs: float, true_peak: float, loudness_range: float, sample_rate: int) -> None:
        logger.info(f'Target Loudness: {lufs} dB LUFS')
        logger.info(f'True Peak: {true_peak} dBFS')
        logger.info(f'Loudness Range: {loudness_range} LU')
        logger.info(f'Sample Rate: {sample_rate} Hz')

        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Use executor.map to parallelize the processing of oggs
            processed_oggs_task_output = executor.map(self.process_ogg,
                                                      self.oggs,
                                                      [lufs] * len(self.oggs),
                                                      [true_peak] * len(self.oggs),
                                                      [loudness_range] * len(self.oggs),
                                                      [sample_rate] * len(self.oggs))

            for processed_file_name in processed_oggs_task_output:
                self.processed_oggs.append(processed_file_name)

            self.song_manager.update_normalized_oggs_list(self.processed_oggs)

        logger.success('Done.')
