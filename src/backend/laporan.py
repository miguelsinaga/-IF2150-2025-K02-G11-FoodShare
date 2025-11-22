# src/repository/laporan_repo.py
from typing import List, Dict
from .csv_manager import CSVManager
import os

# Use project-root-relative safe data path
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.join(ROOT, "tests", "data") 
LAPORAN_CSV = os.path.join(BASE_DIR, "laporan.csv")

_header = ["idLaporan","idRequest","tanggalLaporan","jenisLaporan","deskripsi","estimasiPengurangan"]

class LaporanRepo:
    def __init__(self, path: str = LAPORAN_CSV):
        self._mgr = CSVManager(path, _header)

    def all(self) -> List[Dict]:
        rows = self._mgr.read_all()
        res = []
        for r in rows[1:]:
            res.append({
                "idLaporan": int(r[0]),
                "idRequest": int(r[1]),
                "tanggalLaporan": r[2],
                "jenisLaporan": r[3],
                "deskripsi": r[4],
                "estimasiPengurangan": float(r[5]) if r[5] else 0.0
            })
        return res

    def next_id(self) -> int:
        return self._mgr.next_id()

    def save(self, lap: Dict):
        row = [lap["idLaporan"], lap["idRequest"], lap.get("tanggalLaporan",""), lap.get("jenisLaporan",""), lap.get("deskripsi",""), lap.get("estimasiPengurangan",0.0)]
        self._mgr.append_row(row)
