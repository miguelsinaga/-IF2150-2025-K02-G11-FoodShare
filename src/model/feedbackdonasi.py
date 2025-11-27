# src/model/feedback.py
from dataclasses import dataclass
from datetime import datetime
from src.backend.feedback_data import FeedbackRepo

repo = FeedbackRepo()

@dataclass
class Feedback:
    idFeedback: int
    idProvider: int
    idReceiver: int
    rating: int
    komentar: str
    tanggalFeedback: str = ""

    @staticmethod
    def from_dict(d: dict) -> "Feedback":
        return Feedback(
            idFeedback=d["idFeedback"],
            idProvider=d["idProvider"],
            idReceiver=d["idReceiver"],
            rating=d["rating"],
            komentar=d["komentar"],
            tanggalFeedback=d["tanggalFeedback"]
        )

    @staticmethod
    def all():
        return [Feedback.from_dict(f) for f in repo.all()]

    @staticmethod
    def by_provider(pid: int):
        return [Feedback.from_dict(f) for f in repo.find_by_provider(pid)]

    @staticmethod
    def by_receiver(rid: int):
        return [Feedback.from_dict(f) for f in repo.find_by_receiver(rid)]

    def save(self):
        if not self.tanggalFeedback:
            self.tanggalFeedback = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        repo.save(self.__dict__)

    def update(self):
        repo.update(self.__dict__)

    def ubahKomentar(self, komentarBaru: str):
        self.komentar = komentarBaru
        self.update()

    def ubahRating(self, ratingBaru: int):
        r = int(ratingBaru)
        if r < 1:
            r = 1
        if r > 3:
            r = 3
        self.rating = r
        self.update()

    def tampilkanFeedback(self) -> str:
        try:
            from src.model.user import Pengguna
            p = Pengguna.find_by_id(self.idProvider)
            pname = p.nama if p else f"Provider #{self.idProvider}"
        except Exception:
            pname = f"Provider #{self.idProvider}"
        return f"{pname} Rating {self.rating} {self.komentar}"

    def getRating(self) -> int:
        return self.rating

    def getKomentar(self) -> str:
        return self.komentar
