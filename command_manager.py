import shlex
import subprocess
from pathlib import Path
from typing import List

from loguru import logger


class CommandManager:
    @staticmethod
    def build_normalize_command(song_path: Path, target_level: float, sample_rate: int,
                                temp_output_path: str) -> List[str]:
        command = shlex.split(f'ffmpeg-normalize '
                              f'"{song_path}" '
                              f'-t {target_level} '
                              f'-ar {sample_rate} '
                              f'-o "{temp_output_path}" '
                              f'-c:a libvorbis '
                              f'-q')
        return command

    @staticmethod
    def execute_normalize_command(command: List[str], filename: Path) -> str:
        logger.info(f'Processing {filename.name}')
        return_value = subprocess.run(command)

        return filename.name if return_value.returncode == 0 else ''
