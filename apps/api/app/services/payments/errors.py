class PaymentError(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code


class ProviderDisabledError(PaymentError):
    status_code = 400


class ProviderConfigurationError(PaymentError):
    status_code = 400


class PaymentValidationError(PaymentError):
    status_code = 400


class PaymentNotFoundError(PaymentError):
    status_code = 404
