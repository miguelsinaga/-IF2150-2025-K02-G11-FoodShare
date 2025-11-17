# src/model/feedback.py
from dataclasses import dataclass
from datetime import datetime
from src.backend.feedback import FeedbackRepo

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

    def save(self):
        if not self.tanggalFeedback:
            self.tanggalFeedback = datetime.now().isoformat()
        repo.save(self.__dict__)
