from dataclasses import dataclass
from datetime import datetime
from src.backend.laporan_data import LaporanRepo
from src.model.reqdonasi import RequestDonasi
from src.model.makanan import DataMakanan

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

    def catatLaporan(self):
        if not self.tanggalLaporan:
            self.tanggalLaporan = datetime.now().isoformat()
        self.estimasiPengurangan = self.generateEstimasiPengurangan()
        self.save()

    def generateEstimasiPengurangan(self) -> float:
        req = RequestDonasi.find_by_id(self.idRequest)
        if not req:
            return 0.0
        don = DataMakanan.find_by_id(req.idDonasi)
        if not don:
            return 0.0
        return float(don.jumlahPorsi) * 0.3

    def getDetail(self) -> str:
        return f"Laporan #{self.idLaporan} untuk Request #{self.idRequest} ({self.jenisLaporan})"
