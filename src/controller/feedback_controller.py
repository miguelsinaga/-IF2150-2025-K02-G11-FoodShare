from datetime import datetime
from src.model.feedbackdonasi import Feedback
from src.backend.feedback_data import FeedbackRepo

repo = FeedbackRepo()

class FeedbackController:

    @staticmethod
    def kirimFeedback(idProvider: int, idReceiver: int, rating: int, komentar: str):
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