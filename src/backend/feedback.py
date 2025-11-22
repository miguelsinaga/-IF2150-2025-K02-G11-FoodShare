# src/repository/feedback_repo.py
from typing import List, Dict
from .csv_manager import CSVManager
import os

# Use project-root-relative safe data path
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.join(ROOT, "tests", "data") 
FEEDBACK_CSV = os.path.join(BASE_DIR, "feedback.csv")

_header = ["idFeedback","idProvider","idReceiver","rating","komentar","tanggalFeedback"]

class FeedbackRepo:
    def __init__(self, path: str = FEEDBACK_CSV):
        self._mgr = CSVManager(path, _header)

    def all(self) -> List[Dict]:
        rows = self._mgr.read_all()
        res = []
        for r in rows[1:]:
            res.append({
                "idFeedback": int(r[0]),
                "idProvider": int(r[1]),
                "idReceiver": int(r[2]),
                "rating": int(r[3]),
                "komentar": r[4],
                "tanggalFeedback": r[5]
            })
        return res

    def find_by_provider(self, provider_id: int) -> List[Dict]:
        return [f for f in self.all() if f["idProvider"] == provider_id]

    def next_id(self) -> int:
        return self._mgr.next_id()

    def save(self, fb: Dict):
        row = [fb["idFeedback"], fb["idProvider"], fb["idReceiver"], fb["rating"], fb.get("komentar",""), fb.get("tanggalFeedback","")]
        self._mgr.append_row(row)
