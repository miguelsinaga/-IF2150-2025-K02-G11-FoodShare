from datetime import datetime
from src.model.feedbackdonasi import Feedback
from src.backend.feedback_data import FeedbackRepo
from src.backend.donatur_data import DonaturRepo
from src.backend.penerima_data import PenerimaRepo

repo = FeedbackRepo()

class FeedbackController:

    @staticmethod
    def kirimFeedback(idProvider: int, idReceiver: int, rating: int, komentar: str):
        DonaturRepo().ensure_exists(idProvider)
        PenerimaRepo().ensure_exists(idReceiver)
        fid = repo.next_id()

        fb = Feedback(
            idFeedback=fid,
            idProvider=idProvider,
            idReceiver=idReceiver,
            rating=rating,
            komentar=komentar,
            tanggalFeedback=datetime.now().isoformat()
        )

        fb.save()
        return {"status": "SUCCESS", "message": "Feedback berhasil terkirim", "feedback": fb}

    @staticmethod
    def hitungRataRataProvider(provider_id: int) -> float:
        fbs = Feedback.by_provider(provider_id)
        if not fbs:
            return 0.0
        return sum(f.rating for f in fbs) / len(fbs)
