
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from src.backend.makanan_data import DataMakananRepo

repo = DataMakananRepo()

@dataclass
class DataMakanan:
    idDonasi: int
    idProvider: int
    jenisMakanan: str
    jumlahPorsi: int
    lokasi: str
    batasWaktu: str
    status: str = "Tersedia"
    tanggal_donasi: str = ""

    @staticmethod
    def from_dict(d: dict) -> "DataMakanan":
        return DataMakanan(
            idDonasi=d["idDonasi"],
            idProvider=d["idProvider"],
            jenisMakanan=d["jenisMakanan"],
            jumlahPorsi=d["jumlahPorsi"],
            lokasi=d["lokasi"],
            batasWaktu=d["batasWaktu"],
            status=d["status"],
            tanggal_donasi=d["tanggal_donasi"]
        )

    @staticmethod
    def all():
        return [DataMakanan.from_dict(d) for d in repo.all()]

    @staticmethod
    def find_by_id(idDonasi: int) -> Optional["DataMakanan"]:
        raw = repo.find_by_id(idDonasi)
        return DataMakanan.from_dict(raw) if raw else None

    @staticmethod
    def aktif():
        return [d for d in DataMakanan.all() if d.status.lower() == "tersedia"]

    def save(self):
        if not self.tanggal_donasi:
            self.tanggal_donasi = datetime.now().isoformat()
        repo.save(self.__dict__)

    def update(self):
        repo.update(self.__dict__)
