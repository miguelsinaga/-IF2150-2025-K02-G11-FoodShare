# src/model/requestdonasi.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from src.backend.request_data import RequestRepo

repo = RequestRepo()

@dataclass
class RequestDonasi:
    idRequest: int
    idDonasi: int
    idReceiver: int
    status: str = "Pending"
    tanggalRequest: str = ""

    @staticmethod
    def from_dict(d: dict) -> "RequestDonasi":
        return RequestDonasi(
            idRequest=d["idRequest"],
            idDonasi=d["idDonasi"],
            idReceiver=d["idReceiver"],
            status=d["status"],
            tanggalRequest=d["tanggalRequest"]
        )

    @staticmethod
    def all():
        return [RequestDonasi.from_dict(r) for r in repo.all()]

    @staticmethod
    def find_by_id(idRequest: int) -> Optional["RequestDonasi"]:
        raw = repo.find_by_id(idRequest)
        return RequestDonasi.from_dict(raw) if raw else None

    @staticmethod
    def find_by_receiver(uid: int):
        return [RequestDonasi.from_dict(r) for r in repo.find_by_receiver(uid)]

    def save(self):
        if not self.tanggalRequest:
            self.tanggalRequest = datetime.now().isoformat()
        repo.save(self.__dict__)

    def update(self):
        repo.update(self.__dict__)

    def setStatus(self, status: str):
        self.status = status
        self.update()

    def getStatus(self) -> str:
        return self.status

    def getDetail(self) -> str:
        return f"Request #{self.idRequest} Donasi #{self.idDonasi} Receiver #{self.idReceiver} {self.status}"
