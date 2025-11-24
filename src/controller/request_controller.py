from typing import Dict, List
from datetime import datetime
from src.model.reqdonasi import RequestDonasi
from src.model.makanan import DataMakanan
from src.backend.request import RequestRepo
# PERBAIKAN: Import Pengguna dengan benar
from src.model.user import Pengguna 

repo = RequestRepo()

class RequestController:
    
    @staticmethod
    def buatRequest(idDonasi: int, idReceiver: int):
        donasi = DataMakanan.find_by_id(idDonasi)
        if not donasi:
            return {"status": "FAIL", "message": "Donasi tidak ditemukan"}

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

        donasi.status = "Dipesan"
        donasi.update()

        return {"status": "SUCCESS", "message": "Request berhasil dibuat", "request": req}

    @staticmethod
    def semuaRequest() -> List[RequestDonasi]:
        return RequestDonasi.all()
    
    @staticmethod
    def getRequestByProviderId(provider_id: int) -> List[RequestDonasi]:
        all_donasi = DataMakanan.all()
        provider_donasi_ids = {d.idDonasi for d in all_donasi if str(d.idProvider) == str(provider_id)}
        all_requests = RequestDonasi.all()
        
        provider_requests = [
            req for req in all_requests if req.idDonasi in provider_donasi_ids
        ]
        return provider_requests
    
    @staticmethod
    def updateStatus(idRequest: int, new_status: str) -> Dict:
        req = RequestDonasi.find_by_id(idRequest)
        
        if not req:
            return {"status": "FAIL", "message": f"Request ID {idRequest} tidak ditemukan"}

        donasi = DataMakanan.find_by_id(req.idDonasi)

        if donasi:
            if req.status == "Pending" and new_status == "Preparing":
                donasi.status = "Diproses"
                donasi.update()
            
            elif req.status == "Pending" and new_status == "Rejected":
                donasi.status = "Tersedia" 
                donasi.update()

            elif req.status == "Preparing" and new_status == "On Delivery":
                donasi.status = "Dikirim"
                donasi.update()
            
            # TAMBAHAN LOGIC: On Delivery -> Completed
            elif req.status == "On Delivery" and new_status == "Completed":
                donasi.status = "Selesai" # Atau biarkan "Dikirim" jika history, tapi biasanya donasi dianggap selesai
                donasi.update()

        req.status = new_status
        req.update()
        
        return {"status": "SUCCESS", "message": f"Status Request {idRequest} berhasil diubah ke {new_status}"}
    
    @staticmethod
    def getReceiverName(idReceiver: int) -> str:
        """ Mendapatkan nama receiver berdasarkan ID """
        # PERBAIKAN: Menggunakan Pengguna.find_by_id
        try:
            user = Pengguna.find_by_id(idReceiver) 
            return user.nama if user else f"User #{idReceiver}"
        except Exception:
            return f"User #{idReceiver}"

    @staticmethod
    def getDonasiName(idDonasi: int) -> str:
        donasi = DataMakanan.find_by_id(idDonasi)
        return donasi.jenisMakanan if donasi else f"Donasi #{idDonasi}"