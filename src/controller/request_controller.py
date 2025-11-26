from datetime import datetime
from src.model.reqdonasi import RequestDonasi
from src.model.makanan import DataMakanan
from src.backend.request_data import RequestRepo
from src.backend.penerima_data import PenerimaRepo

repo = RequestRepo()

class RequestController:

    @staticmethod
    def buatRequest(idDonasi: int, idReceiver: int):
        PenerimaRepo().ensure_exists(idReceiver)
        donasi = DataMakanan.find_by_id(idDonasi)
        if not donasi:
            return {"status": "FAIL", "message": "Donasi tidak ditemukan"}

        if donasi.status.lower() != "tersedia":
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

        # Update donasi menjadi dipesan
        donasi.status = "Dipesan"
        donasi.update()

        return {"status": "SUCCESS", "message": "Request berhasil dibuat", "request": req}

    @staticmethod
    def semuaRequest():
        return RequestDonasi.all()

    @staticmethod
    def getRequestByProviderId(provider_id: int):
        """Get all requests related to donations from a provider"""
        all_requests = RequestDonasi.all()
        provider_donasi_ids = []
        
        all_donasi = DataMakanan.all()
        for donasi in all_donasi:
            donasi_provider_id = getattr(donasi, 'idProvider', getattr(donasi, 'provider_id', getattr(donasi, 'id_provider', None)))
            if donasi_provider_id is not None and str(donasi_provider_id) == str(provider_id):
                provider_donasi_ids.append(donasi.idDonasi)
        
        return [req for req in all_requests if req.idDonasi in provider_donasi_ids]

    @staticmethod
    def updateStatus(request_id: int, new_status: str):
        """Update the status of a request"""
        request = RequestDonasi.find_by_id(request_id)
        if not request:
            return {"status": "FAIL", "message": "Request tidak ditemukan"}
        
        request.status = new_status
        request.update()
        
        # If status is Completed, update donasi status too
        if new_status == "Completed":
            donasi = DataMakanan.find_by_id(request.idDonasi)
            if donasi:
                donasi.status = "Completed"
                donasi.update()
        
        return {"status": "SUCCESS", "message": f"Status request berhasil diubah menjadi {new_status}"}

    @staticmethod
    def getDonasiName(donasi_id: int):
        """Get food item name from donation ID"""
        donasi = DataMakanan.find_by_id(donasi_id)
        if donasi:
            return donasi.jenisMakanan
        return f"Unknown (ID: {donasi_id})"

    @staticmethod
    def getReceiverName(receiver_id: int):
        """Get receiver name from receiver ID"""
        from src.model.user import Pengguna
        user = Pengguna.find_by_id(receiver_id)
        if user:
            return user.nama
        return f"Unknown Receiver (ID: {receiver_id})"
