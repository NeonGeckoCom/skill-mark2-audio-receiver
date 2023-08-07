# pylint: disable=missing-function-docstring
from subprocess import CalledProcessError
from unittest.mock import call, patch, Mock

import pytest

from skill_mark2_audio_receiver.pair import (
    auto_pair_bluetooth,
    auto_pair_kdeconnect,
)


def test_auto_pair_bluetooth():
    with patch("subprocess.run", return_value=Mock(returncode=0)) as mock_run:
        auto_pair_bluetooth()
    mock_run.assert_called_with("/usr/local/bin/bluetooth-agent.sh", check=True)


def test_auto_pair_bluetooth_exception():
    with patch("subprocess.run", side_effect=CalledProcessError(1, "/usr/local/bin/bluetooth-agent.sh")):
        with pytest.raises(CalledProcessError):
            auto_pair_bluetooth()


def test_auto_pair_kdeconnect():
    with patch("subprocess.run", return_value=Mock(returncode=0)) as mock_run, patch("time.sleep", return_value=None):
        auto_pair_kdeconnect()
    mock_run.assert_has_calls(
        [
            call(["sudo", "systemctl", "start", "pair-kdeconnect.service"], check=True),
            call(["sudo", "systemctl", "stop", "pair-kdeconnect.service"], check=True),
        ]
    )


def test_auto_pair_kdeconnect_exception():
    with patch(
        "subprocess.run", side_effect=CalledProcessError(1, "sudo systemctl start pair-kdeconnect.service")
    ), patch("time.sleep", return_value=None):
        with pytest.raises(CalledProcessError):
            auto_pair_kdeconnect()
