import sys
from pathlib import Path
from typing import List

from loguru import logger


class SongManager:
    @staticmethod
    def find_songs(input_directory_path: Path) -> List[Path]:
        songs = []
        if not input_directory_path.exists():
            logger.critical('Invalid directory path.')
            sys.exit(1)

        for path in Path(input_directory_path).rglob('song/*.ogg'):
            songs.append(path)

        return songs

    @staticmethod
    def load_normalized_songs() -> List[str]:
        with open('processed_songs.txt', 'r', encoding='utf-8') as f:
            return [song.strip() for song in f]

    @staticmethod
    def update_normalized_songs_file(record: str):
        with open('processed_songs.txt', 'a+', encoding='utf-8') as f:
            if record.strip():
                f.write(f'{record.strip()}\n')
