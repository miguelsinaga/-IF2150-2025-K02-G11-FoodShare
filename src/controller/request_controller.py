from datetime import datetime
from src.model.reqdonasi import RequestDonasi
from src.model.makanan import DataMakanan
from src.backend.request import RequestRepo

repo = RequestRepo()

class RequestController:

    @staticmethod
    def buatRequest(idDonasi: int, idReceiver: int):
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
