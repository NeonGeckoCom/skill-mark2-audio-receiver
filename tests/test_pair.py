# pylint: disable=missing-function-docstring
from unittest.mock import patch, call

import pytest

from skill_mark2_audio_receiver.pair import (
    auto_pair_bluetooth,
    auto_pair_kdeconnect,
)


def test_auto_pair_bluetooth():
    with patch("subprocess.run", return_value=Mock(returncode=0)) as mock_run:
        auto_pair_bluetooth()
    mock_run.assert_called_with("/usr/local/bin/bluetooth-agent.sh")

def test_auto_pair_bluetooth_exception():
    with patch("subprocess.run", return_value=Mock(returncode=1)) as mock_run:
        with pytest.raises(CalledProcessError):
            auto_pair_bluetooth()
