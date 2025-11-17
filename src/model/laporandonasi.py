# src/model/laporandonasi.py
from dataclasses import dataclass
from datetime import datetime
from src.backend.laporan import LaporanRepo

repo = LaporanRepo()

@dataclass
class LaporanDonasi:
    idLaporan: int
    idRequest: int
    tanggalLaporan: str
    jenisLaporan: str
    deskripsi: str
    estimasiPengurangan: float = 0.0

    @staticmethod
    def from_dict(d: dict) -> "LaporanDonasi":
        return LaporanDonasi(
            idLaporan=d["idLaporan"],
            idRequest=d["idRequest"],
            tanggalLaporan=d["tanggalLaporan"],
            jenisLaporan=d["jenisLaporan"],
            deskripsi=d["deskripsi"],
            estimasiPengurangan=d["estimasiPengurangan"]
        )

    @staticmethod
    def all():
        return [LaporanDonasi.from_dict(l) for l in repo.all()]

    def save(self):
        repo.save(self.__dict__)
