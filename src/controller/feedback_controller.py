from datetime import datetime
import logging
from src.model.feedbackdonasi import Feedback
from src.backend.feedback_data import FeedbackRepo
from src.backend.donatur_data import DonaturRepo
from src.backend.penerima_data import PenerimaRepo

repo = FeedbackRepo()

class FeedbackController:

    @staticmethod
    def kirimFeedback(idProvider: int, idReceiver: int, rating: int, komentar: str):
        komentar = (komentar or "").strip()
        try:
            r_int = int(rating)
        except Exception:
            return {"status": "FAIL", "message": "Rating harus berupa angka 1, 2, atau 3"}
        if r_int not in {1, 2, 3}:
            return {"status": "FAIL", "message": "Rating harus 1, 2, atau 3"}
        DonaturRepo().ensure_exists(idProvider)
        PenerimaRepo().ensure_exists(idReceiver)
        fid = repo.next_id()

        fb = Feedback(
            idFeedback=fid,
            idProvider=idProvider,
            idReceiver=idReceiver,
            rating=r_int,
            komentar=komentar,
            tanggalFeedback=datetime.now().isoformat()
        )
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info("feedback_controller_save_start idFeedback=%s provider_id=%s receiver_id=%s", fid, idProvider, idReceiver)
        fb.save()
        logger.info("feedback_controller_save_success idFeedback=%s provider_id=%s receiver_id=%s", fid, idProvider, idReceiver)
        try:
            FeedbackController.check_and_ban_provider(idProvider)
        except Exception:
            pass
        return {"status": "SUCCESS", "message": "Feedback berhasil terkirim", "feedback": fb}

    @staticmethod
    def hitungRataRataProvider(provider_id: int) -> float:
        fbs = Feedback.by_provider(provider_id)
        if not fbs:
            try:
                FeedbackController.check_and_ban_provider(provider_id)
            except Exception:
                pass
            return 0.0
        avg = sum(f.rating for f in fbs) / len(fbs)
        try:
            FeedbackController.check_and_ban_provider(provider_id)
        except Exception:
            pass
        return avg

    @staticmethod
    def check_and_ban_provider(provider_id: int):
        fbs = Feedback.by_provider(provider_id)
        count = len(fbs)
        avg = (sum(f.rating for f in fbs) / count) if count > 0 else 0.0
        if count >= 5 and avg < 2:
            from src.model.user import Pengguna
            from src.backend.donatur_data import DonaturRepo
            user = Pengguna.find_by_id(provider_id)
            if user and str(user.status).lower() != "banned":
                user.status = "banned"
                user.update()
                try:
                    DonaturRepo().update_status(provider_id, "banned")
                except Exception:
                    pass
                logging.getLogger(__name__).info("auto_ban_provider provider_id=%s count=%s avg=%.2f", provider_id, count, avg)
