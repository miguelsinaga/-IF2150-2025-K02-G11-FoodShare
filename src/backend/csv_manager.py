import csv
import os
import logging
from typing import List

logger = logging.getLogger(__name__)


class CSVManager:
    def __init__(self, filepath: str, header: List[str]):
        self.filepath = filepath
        self.header = header

        base_folder = os.path.dirname(filepath)
        if base_folder and not os.path.exists(base_folder):
            try:
                os.makedirs(base_folder, exist_ok=True)
            except Exception:
                logger.exception("Failed to create base folder for %s", filepath)

        if not os.path.exists(filepath):
            try:
                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
            except Exception:
                logger.exception("Failed to create CSV file %s", filepath)

    def read_all(self) -> List[List[str]]:
        try:
            with open(self.filepath, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)
                return rows if rows else [self.header]
        except Exception:
            logger.exception("Failed to read CSV %s", self.filepath)
            return [self.header]

    def write_all(self, rows: List[List[str]]):
        try:
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            logger.debug("Wrote %d rows to %s", len(rows), self.filepath)
        except Exception:
            logger.exception("Failed to write CSV %s", self.filepath)

    def append_row(self, row: List[str]):
        try:
            with open(self.filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(row)
            logger.debug("Appended row to %s: %s", self.filepath, row)
        except Exception:
            logger.exception("Failed to append row to CSV %s", self.filepath)

    def next_id(self) -> int:
        rows = self.read_all()
        try:
            if len(rows) <= 1:
                return 1
            last_row = rows[-1]
            last_id = int(last_row[0])
            return last_id + 1
        except Exception:
            logger.exception("Failed to compute next_id for %s", self.filepath)
            return 1
