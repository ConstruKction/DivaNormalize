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
        self.processed_files = []

    def load_processed_files(self, record_file):
        try:
            logger.info('Loading already processed records...')

            with open(record_file, 'r') as f:
                for item in f:
                    self.processed_files.append(item)
        except FileNotFoundError:
            pass

    def save_processed_files(self, record_file):
        with open(record_file, 'a+') as f:
            for item in self.processed_files:
                f.write(f'{item}\n')

    def find_oggs(self):
        for path in Path(self.mods_dir_path).rglob('song/*.ogg'):
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
            if f'{ogg.name}\n' in self.processed_files:
                logger.info(f'Song {ogg.name} is already normalized. Skipping to the next song.')
                continue

            temp_output_path = str(Path(tempfile.mkdtemp()) / ogg.name)

            command = self.build_command(ogg, lufs, sample_rate, temp_output_path)
            self.execute_command(command, ogg)

            shutil.move(temp_output_path, ogg)  # Rename the temp file to overwrite the original

            self.processed_files.append(ogg.name)
            logger.info(f'Song {ogg.name} normalized and saved in the known records')

        self.save_processed_files('processed_songs.txt')

        logger.info('Done.')
