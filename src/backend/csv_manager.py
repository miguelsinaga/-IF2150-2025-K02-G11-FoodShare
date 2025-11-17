# src/backend/csv_manager.py
import csv
import os

class CSVManager:
    def __init__(self, filepath, header):
        self.filepath = filepath
        self.header = header
        if not os.path.exists(filepath):
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(header)

    def read_all(self):
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            return list(reader)

    def write_all(self, rows):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def append_row(self, row):
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
