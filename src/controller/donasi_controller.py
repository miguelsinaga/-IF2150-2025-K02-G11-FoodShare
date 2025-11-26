from typing import Dict
from datetime import datetime
from src.model.makanan import DataMakanan
from src.backend.makanan_data import DataMakananRepo

repo = DataMakananRepo()

class DonasiController:

    @staticmethod
    def buatDonasi(idProvider: int, data: Dict) -> Dict:
        """
        data = {
            "jenisMakanan": ...,
            "jumlahPorsi": ...,
            "lokasi": ...,
            "batasWaktu": "YYYY-MM-DD"
        }
        """
        did = repo.next_id()

        donasi = DataMakanan(
            idDonasi=did,
            idProvider=idProvider,
            jenisMakanan=data["jenisMakanan"],
            jumlahPorsi=int(data["jumlahPorsi"]),
            lokasi=data["lokasi"],
            batasWaktu=data["batasWaktu"],
            status="Tersedia",
            tanggal_donasi=datetime.now().isoformat()
        )

        donasi.save()
        return {"status": "SUCCESS", "message": "Donasi berhasil dibuat", "donasi": donasi}

    @staticmethod
    def getDonasiAktif():
        return DataMakanan.aktif()

    @staticmethod
    def semuaDonasi():
        """Get all donations"""
        return DataMakanan.all()

    @staticmethod
    def updateDonasi(data: Dict) -> Dict:
        """
        Update existing donation
        data = {
            "idDonasi": ...,
            "jenisMakanan": ...,
            "jumlahPorsi": ...,
            "lokasi": ...,
            "batasWaktu": "YYYY-MM-DD"
        }
        """
        donasi = DataMakanan.find_by_id(data["idDonasi"])
        if not donasi:
            return {"status": "FAIL", "message": "Donasi tidak ditemukan"}
        
        donasi.jenisMakanan = data["jenisMakanan"]
        donasi.jumlahPorsi = int(data["jumlahPorsi"])
        donasi.lokasi = data["lokasi"]
        donasi.batasWaktu = data["batasWaktu"]
        donasi.update()
        
        return {"status": "SUCCESS", "message": "Donasi berhasil diperbarui", "donasi": donasi}

    @staticmethod
    def batalkanDonasi(idDonasi: int) -> Dict:
        donasi = DataMakanan.find_by_id(idDonasi)

        if not donasi:
            return {"status": "FAIL", "message": "Donasi tidak ditemukan"}

        donasi.status = "Dibatalkan"
        donasi.update()

        return {"status": "SUCCESS", "message": "Donasi berhasil dibatalkan"}