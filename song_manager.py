from typing import List


class SongManager:
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
