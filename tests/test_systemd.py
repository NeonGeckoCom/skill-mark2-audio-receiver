from subprocess import CalledProcessError

import pytest

from skill_mark2_audio_receiver.systemd import (
    get_service_status,
    interact_with_service,
    normalize_service_name,
    reload_daemon,
)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("bluetooth", "bluetooth.service"),
        ("bluetooth.service", "bluetooth.service"),
        ("bluetooth.serv", "bluetooth.serv.service"),
        ("raspotify", "raspotify.service"),
        ("raspotify.service", "raspotify.service"),
        ("raspotify.serv", "raspotify.serv.service"),
        ("uxplay", "uxplay.service"),
        ("uxplay.service", "uxplay.service"),
        ("uxplay.serv", "uxplay.serv.service"),
    ],
)
def test_normalize_service_name(name, expected):
    assert normalize_service_name(name) == expected


def test_interact_with_service():
    # TODO: Set up a fake service to work with for testing
    for command in ("disable", "enable", "start", "restart"):
        assert interact_with_service("bluetooth", command) is True
    # Test invalid command verb
    with pytest.raises(CalledProcessError):
        interact_with_service("bluetooth", "bananas")
    # Test non-existent service and non-existent verb
    with pytest.raises(CalledProcessError):
        interact_with_service("mxyzptlk", "restart")
        interact_with_service("mxyzptlk", "engage")


def test_reload_daemon():
    assert reload_daemon() is True


def test_status():
    status = get_service_status("bluetooth")
    assert isinstance(status, str)
    assert "bluetooth.service" in status
