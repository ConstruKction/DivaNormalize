import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from loguru import logger


class AudioProcessor:
    def __init__(self, mods_dir_path):
        self.mods_dir_path = mods_dir_path
        self.oggs = []
        self.processed_files = set()

        logger.remove()
        logger.add(sys.stdout, level="INFO")

    def load_processed_files(self, record_file):
        try:
            logger.info('Loading already processed records...')

            with open(record_file, 'r') as f:
                # Convert lines to a set
                self.processed_files = set(map(str.strip, f.readlines()))

        except FileNotFoundError:
            pass  # No file = no big deal, program will continue and create one

    def save_processed_files(self, record_file):
        # Convert a set to a list before saving
        processed_list = list(self.processed_files)
        with open(record_file, 'w') as f:
            for item in processed_list:
                f.write(f'{item}\n')

    def find_oggs(self):
        if not self.mods_dir_path.exists():
            logger.critical('Invalid mod directory path.')
            sys.exit(1)

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

        for ogg in list(self.oggs):  # Create a copy of the set to avoid modification during iteration
            if f'{ogg.name}' in self.processed_files:
                logger.warning(f'Song {ogg.name} is already normalized. Skipping to the next song.')
            else:
                temp_output_path = str(Path(tempfile.mkdtemp()) / ogg.name)

                command = self.build_command(ogg, lufs, sample_rate, temp_output_path)
                self.execute_command(command, ogg)

                shutil.move(temp_output_path, ogg)  # Rename the temp file to overwrite the original

                self.processed_files.add(ogg.name)
                logger.info(f'Song {ogg.name} normalized and saved in the known records')

                self.save_processed_files('processed_songs.txt')

        logger.info('Done.')
