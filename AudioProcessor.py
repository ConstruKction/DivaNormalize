import json
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path

from loguru import logger


class AudioProcessor:
    def __init__(self, mods_dir_path):
        self.mods_dir_path = mods_dir_path
        self.oggs = []
        self.processed_files = set()

    oggs = []

    def load_processed_files(self, record_file):
        try:
            logger.info('Loading already processed records.')

            with open(record_file, 'r') as f:
                self.processed_files = set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_processed_files(self, record_file):
        with open(record_file, 'w') as f:
            json.dump(list(self.processed_files), f)

        logger.info('Song normalized and saved in the record.')

    def find_oggs(self):
        for path in self.mods_dir_path.rglob('song/*.ogg'):
            self.oggs.append(path)

    @staticmethod
    def build_command(ogg_path, lufs, sample_rate, temp_output_path):
        command = shlex.split(f'ffmpeg -loglevel quiet -i "{ogg_path}" -filter:a loudnorm=linear=true:i={lufs} '
                              f'-ar {sample_rate} "{temp_output_path}"')
        return command

    @staticmethod
    def execute_command(command, filename):
        subprocess.run(command)
        logger.info(f'Normalizing {filename.name}')

    def process_oggs(self, lufs, sample_rate):
        logger.info(f'LUFS: {lufs}')

        for ogg in self.oggs:
            if ogg not in self.processed_files:
                temp_output_path = str(Path(tempfile.mkdtemp()) / ogg.name)
                command = self.build_command(ogg, lufs, sample_rate, temp_output_path)
                self.execute_command(command, ogg)
                shutil.move(temp_output_path, ogg)  # Rename the temp file to overwrite the original
                self.processed_files.add(ogg)

        self.save_processed_files('processed_songs.json')
