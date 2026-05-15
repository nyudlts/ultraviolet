from ultraviolet.entraid.oauth import _email_to_username


def test_email_to_username():
    assert _email_to_username("bk3107@nyu.edu") == "nyu-bk3107"
