from typing import Dict
from datetime import datetime
from src.model.makanan import DataMakanan
from src.backend.makanan_data import DataMakananRepo
from src.controller.request_controller import RequestController
from src.backend.donatur_data import DonaturRepo
from src.constants.locations import BANDUNG_LOCATIONS

repo = DataMakananRepo()

class DonasiController:

    @staticmethod
    def is_valid_location(lokasi: str) -> bool:
        """Validate if location is in allowed Bandung locations"""
        return lokasi in BANDUNG_LOCATIONS

    @staticmethod
    def buatDonasi(idProvider: int, data: Dict) -> Dict:
        DonaturRepo().ensure_exists(idProvider)
        """
        data = {
            "jenisMakanan": ...,
            "jumlahPorsi": ...,
            "lokasi": ..., 
            "batasWaktu": "YYYY-MM-DD"
        }
        """
        # Validate location
        if not DonasiController.is_valid_location(data["lokasi"]):
            return {"status": "FAIL", "message": f"Lokasi '{data['lokasi']}' tidak valid. Silakan pilih dari daftar lokasi Bandung yang tersedia."}
        
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
        # Validate location
        if not DonasiController.is_valid_location(data["lokasi"]):
            return {"status": "FAIL", "message": f"Lokasi '{data['lokasi']}' tidak valid. Silakan pilih dari daftar lokasi Bandung yang tersedia."}
        
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

    @staticmethod
    def prosesBuatDonasi(idProvider: int, data: Dict) -> Dict:
        return DonasiController.buatDonasi(idProvider, data)

    @staticmethod
    def prosesEditDonasi(data: Dict) -> Dict:
        return DonasiController.updateDonasi(data)

    @staticmethod
    def prosesBatalkanDonasi(idDonasi: int) -> Dict:
        return DonasiController.batalkanDonasi(idDonasi)

    @staticmethod
    def prosesBuatRequest(idDonasi: int, idReceiver: int) -> Dict:
        return RequestController.buatRequest(idDonasi, idReceiver)
