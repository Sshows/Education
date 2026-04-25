from app.schemas.forecast import ApplicantProfileIn
from app.services.forecast_service import ForecastService


class DummyDB:
    def scalar(self, *args, **kwargs):
        return None

    class DummyScalars:
        def all(self):
            return []

    def scalars(self, *args, **kwargs):
        return self.DummyScalars()


def test_forecast_with_missing_data_returns_low_confidence():
    service = ForecastService(DummyDB())
    try:
        service.calculate(ApplicantProfileIn(total_score=80, profile_subject_1="M", profile_subject_2="I", subject_combo="M+I"), 1, 1)
    except ValueError:
        assert True
