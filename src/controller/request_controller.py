from typing import Dict, List
from datetime import datetime
from src.model.reqdonasi import RequestDonasi
from src.model.makanan import DataMakanan
from src.backend.request import RequestRepo
# Asumsi: Anda memiliki User Model yang bisa di-import (sesuai file sebelumnya)
from src.model.user import Pengguna

repo = RequestRepo()

class RequestController:
    
    @staticmethod
    def buatRequest(idDonasi: int, idReceiver: int):
        donasi = DataMakanan.find_by_id(idDonasi)
        if not donasi:
            return {"status": "FAIL", "message": "Donasi tidak ditemukan"}

        # Cek status 'Dipesan' (jika sudah di-request sebelumnya) atau 'Tersedia'
        if donasi.status.lower() not in ["tersedia"]:
            return {"status": "FAIL", "message": "Donasi sudah diambil / tidak tersedia"}

        rid = repo.next_id()

        req = RequestDonasi(
            idRequest=rid,
            idDonasi=idDonasi,
            idReceiver=idReceiver,
            status="Pending",
            tanggalRequest=datetime.now().isoformat()
        )

        req.save()

        # Update donasi menjadi dipesan (selama masih Pending, status Donasi = Dipesan)
        donasi.status = "Dipesan"
        donasi.update()

        return {"status": "SUCCESS", "message": "Request berhasil dibuat", "request": req}

    @staticmethod
    def semuaRequest() -> List[RequestDonasi]:
        """ Mengambil semua request donasi """
        return RequestDonasi.all()
    
    @staticmethod
    def getRequestByProviderId(provider_id: int) -> List[RequestDonasi]:
        """
        Mengambil semua request yang terkait dengan donasi dari provider tertentu.
        Ini menggabungkan data request dan donasi.
        """
        all_donasi = DataMakanan.all()
        # Menggunakan set comprehension untuk efisiensi
        provider_donasi_ids = {d.idDonasi for d in all_donasi if str(d.idProvider) == str(provider_id)}
        
        all_requests = RequestDonasi.all()
        
        # Filter request yang idDonasi-nya milik provider ini
        provider_requests = [
            req for req in all_requests if req.idDonasi in provider_donasi_ids
        ]
        return provider_requests
    
    @staticmethod
    def updateStatus(idRequest: int, new_status: str) -> Dict:
        """
        Memperbarui status request donasi.
        new_status bisa berupa: "Preparing", "On Delivery", "Completed", "Rejected".
        """
        req = RequestDonasi.find_by_id(idRequest)
        
        if not req:
            return {"status": "FAIL", "message": f"Request ID {idRequest} tidak ditemukan"}

        donasi = DataMakanan.find_by_id(req.idDonasi)

        # Logika sinkronisasi status Donasi berdasarkan aksi Request
        if donasi:
            if req.status == "Pending" and new_status == "Preparing":
                # Accept: Request Pending -> Preparing, Donasi Dipesan -> Diproses
                donasi.status = "Diproses"
                donasi.update()
            
            elif req.status == "Pending" and new_status == "Rejected":
                # Reject: Request Pending -> Rejected, Donasi Dipesan -> Tersedia
                donasi.status = "Tersedia" 
                donasi.update()

            elif req.status == "Preparing" and new_status == "On Delivery":
                # Ready for Delivery: Request Preparing -> On Delivery, Donasi Diproses -> Dikirim
                donasi.status = "Dikirim"
                donasi.update()


        # Perbarui status request
        req.status = new_status
        req.update()
        
        return {"status": "SUCCESS", "message": f"Status Request {idRequest} berhasil diubah ke {new_status}"}
    
    @staticmethod
    def getReceiverName(idReceiver: int) -> str:
        """ Mendapatkan nama receiver berdasarkan ID (untuk display di tabel) """
        # Asumsi: Anda memiliki User Model/Repo yang bisa mencari user
        try:
            # Menggunakan User.find_by_id() (asumsi User model sudah ada)
            user = User.find_by_id(idReceiver) 
            return user.nama if user else f"User #{idReceiver}"
        except Exception:
            # Fallback jika model atau find_by_id error
            return f"User #{idReceiver}"

    @staticmethod
    def getDonasiName(idDonasi: int) -> str:
        """ Mendapatkan nama donasi berdasarkan ID (untuk display di tabel) """
        donasi = DataMakanan.find_by_id(idDonasi)
        return donasi.jenisMakanan if donasi else f"Donasi #{idDonasi}"