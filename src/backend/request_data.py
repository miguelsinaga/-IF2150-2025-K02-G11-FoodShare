from typing import List, Dict, Optional
from .csv_manager import CSVManager
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.join(ROOT, "data")
REQUESTS_CSV = os.path.join(BASE_DIR, "requests.csv")

_header = ["idRequest","idDonasi","idReceiver","status","tanggalRequest"]

class RequestRepo:
    def __init__(self, path: str = REQUESTS_CSV):
        self._mgr = CSVManager(path, _header)

    def all(self) -> List[Dict]:
        rows = self._mgr.read_all()
        res = []
        for r in rows[1:]:
            res.append({
                "idRequest": int(r[0]),
                "idDonasi": int(r[1]),
                "idReceiver": int(r[2]),
                "status": r[3],
                "tanggalRequest": r[4]
            })
        return res

    def find_by_id(self, idRequest: int) -> Optional[Dict]:
        for req in self.all():
            if req["idRequest"] == idRequest:
                return req
        return None

    def find_by_receiver(self, receiver_id: int) -> List[Dict]:
        return [r for r in self.all() if r["idReceiver"] == receiver_id]

    def next_id(self) -> int:
        return self._mgr.next_id()

    def save(self, req: Dict):
        row = [req["idRequest"], req["idDonasi"], req["idReceiver"], req.get("status","Pending"), req.get("tanggalRequest","")]
        self._mgr.append_row(row)

    def update(self, req: Dict):
        rows = self._mgr.read_all()
        header = rows[0]
        new = [header]
        for r in rows[1:]:
            if int(r[0]) == int(req["idRequest"]):
                new.append([req["idRequest"], req["idDonasi"], req["idReceiver"], req.get("status","Pending"), req.get("tanggalRequest","")])
            else:
                new.append(r)
        self._mgr.write_all(new)
