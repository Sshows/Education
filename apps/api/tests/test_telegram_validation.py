from app.utils.telegram import validate_telegram_init_data


def test_invalid_init_data_rejected():
    assert not validate_telegram_init_data("user=%7B%7D", "token")
