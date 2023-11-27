import shlex
import subprocess
from pathlib import Path
from typing import List

from loguru import logger


class CmdManager:

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
        logger.info(f'Processing {filename.name}')
        return_value = subprocess.run(command)

        return filename.name if return_value.returncode == 0 else ''
