import csv
import os
from typing import List

class CSVManager:
    def __init__(self, path: str, header: List[str]):
        self.path = path
        self.header = header
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)

    def read_all(self) -> List[List[str]]:
        with open(self.path, newline='', encoding='utf-8') as f:
            return list(csv.reader(f))

    def write_all(self, rows: List[List[str]]):
        with open(self.path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def append_row(self, row: List[str]):
        with open(self.path, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def next_id(self) -> int:
        rows = self.read_all()
        if len(rows) <= 1:
            return 1
        last_id = rows[-1][0]
        try:
            return int(last_id) + 1
        except:
            return len(rows)
