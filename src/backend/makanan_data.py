from typing import List, Dict, Optional
from .csv_manager import CSVManager
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.join(ROOT, "data")
DONASI_CSV = os.path.join(BASE_DIR, "donasi.csv")

_header = ["idDonasi","idProvider","jenisMakanan","jumlahPorsi","lokasi","batasWaktu","status","tanggal_donasi"]

class DataMakananRepo:
    def __init__(self, path: str = DONASI_CSV):
        self._mgr = CSVManager(path, _header)

    def all(self) -> List[Dict]:
        rows = self._mgr.read_all()
        res = []
        for r in rows[1:]:
            res.append({
                "idDonasi": int(r[0]),
                "idProvider": int(r[1]),
                "jenisMakanan": r[2],
                "jumlahPorsi": int(r[3]),
                "lokasi": r[4],
                "batasWaktu": r[5],
                "status": r[6],
                "tanggal_donasi": r[7]
            })
        return res

    def find_by_id(self, idDonasi: int) -> Optional[Dict]:
        for d in self.all():
            if d["idDonasi"] == idDonasi:
                return d
        return None

    def find_by_status(self, status: str) -> List[Dict]:
        return [d for d in self.all() if d["status"].lower() == status.lower()]

    def find_by_provider(self, provider_id: int) -> List[Dict]:
        return [d for d in self.all() if d["idProvider"] == provider_id]

    def next_id(self) -> int:
        return self._mgr.next_id()

    def save(self, data: Dict):
        row = [data["idDonasi"], data["idProvider"], data["jenisMakanan"], data["jumlahPorsi"], data["lokasi"], data["batasWaktu"], data.get("status","Tersedia"), data.get("tanggal_donasi","")]
        self._mgr.append_row(row)

    def update(self, data: Dict):
        rows = self._mgr.read_all()
        header = rows[0]
        new = [header]
        for r in rows[1:]:
            if int(r[0]) == int(data["idDonasi"]):
                new.append([data["idDonasi"], data["idProvider"], data["jenisMakanan"], data["jumlahPorsi"], data["lokasi"], data["batasWaktu"], data.get("status","Tersedia"), data.get("tanggal_donasi","")])
            else:
                new.append(r)
        self._mgr.write_all(new)
