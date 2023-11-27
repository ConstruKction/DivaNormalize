import concurrent.futures
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

from loguru import logger


class AudioProcessor:
    def __init__(self, mods_dir_path: Path):
        self.mods_dir_path = mods_dir_path
        self.oggs: List[Path] = []
        self.processed_oggs: List[str] = []

        logger.remove()
        logger.add(sys.stdout, level="INFO")

    @staticmethod
    def load_normalized_oggs() -> List[str]:
        with open('processed_songs.txt', 'r', encoding='utf-8') as f:
            return [song.strip() for song in f]

    @staticmethod
    def update_normalized_oggs_list(records: List[str]) -> None:
        with open('processed_songs.txt', 'a', encoding='utf-8') as f:
            for record in records:
                if record.strip():
                    f.write(f'{record.strip()}\n')

    def find_oggs(self) -> None:
        if not self.mods_dir_path.exists():
            logger.critical('Invalid mod directory path.')
            sys.exit(1)

        for path in Path(self.mods_dir_path).rglob('song/*.ogg'):
            self.oggs.append(path)

    @staticmethod
    def build_command(ogg_path: Path, lufs: float, true_peak: float, loudness_range: float, sample_rate: int,
                      temp_output_path: str) -> List[str]:
        command = shlex.split(f'ffmpeg '
                              f'-loglevel fatal '
                              f'-i "{ogg_path}" '
                              f'-filter:a loudnorm=I={lufs}:TP={true_peak}:LRA={loudness_range} '
                              f'-ar {sample_rate} '
                              f'"{temp_output_path}"')
        return command

    @staticmethod
    def execute_command(command: List[str], filename: Path) -> str:
        logger.info(f'Normalizing {filename.name}')
        return_value = subprocess.run(command)

        return filename.name if return_value.returncode == 0 else ''

    def process_ogg(self, ogg: Path, lufs: float, true_peak: float, loudness_range: float, sample_rate: int) -> str:
        if ogg.name in self.load_normalized_oggs():
            logger.warning(f'{ogg.name} was normalized before -> skipping.')
            return ''

        temp_output_path = str(Path(tempfile.mkdtemp()) / ogg.name)

        command = self.build_command(ogg, lufs, true_peak, loudness_range, sample_rate, temp_output_path)
        processed_ogg_filename = self.execute_command(command, ogg)

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

            self.update_normalized_oggs_list(self.processed_oggs)

        logger.success('Done.')
