# pylint: disable=missing-function-docstring
import pytest
from unittest.mock import patch, Mock
from subprocess import CalledProcessError

from skill_mark2_audio_receiver.systemd import (
    get_service_status,
    interact_with_service,
    modify_exec_start,
    normalize_service_name,
    reload_daemon,
    set_system_service_exec_start,
)

# Unit Tests


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
    with patch("subprocess.run", return_value=Mock(returncode=0)):
        for command in ("disable", "enable", "start", "restart"):
            assert interact_with_service("bluetooth", command) is True

    with patch("subprocess.run", side_effect=CalledProcessError(1, "cmd")):
        with pytest.raises(CalledProcessError):
            interact_with_service("bluetooth", "bananas")
        with pytest.raises(CalledProcessError):
            interact_with_service("mxyzptlk", "restart")
            interact_with_service("mxyzptlk", "engage")


def test_reload_daemon():
    with patch("subprocess.run", return_value=Mock(returncode=0)):
        assert reload_daemon() is True


def test_status():
    mock_output = "bluetooth.service - Bluetooth service"
    with patch("subprocess.run", return_value=Mock(returncode=0, stdout=mock_output.encode("utf-8"))):
        status = get_service_status("bluetooth")
        assert isinstance(status, bool)
        assert status is True


def test_modify_exec_start():
    content = [
        "[Service]\n",
        "User=neon\n",
        "ExecStart=/usr/bin/previous_command --previous-arg\n",
        "Restart=on-failure\n",
    ]
    command = "/usr/bin/new_command"
    args = "--new-arg"

    modified_content = modify_exec_start(content, command, args)
    assert "ExecStart=/usr/bin/new_command --new-arg\n" in modified_content


@patch("skill_mark2_audio_receiver.systemd.reload_daemon")
@patch("skill_mark2_audio_receiver.systemd.interact_with_service")
def test_set_system_service_exec_start(mock_restart, mock_reload, tmpdir):
    service_content = ["[Service]\n", "User=neon\n", "ExecStart=/usr/bin/previous_command\n", "Restart=on-failure\n"]
    service_name = "test_service"
    service_file = tmpdir.join(f"{service_name}.service")
    service_file.write("\n".join(service_content))
    command = "/usr/bin/new_command"
    args = "--new-arg"

    result = set_system_service_exec_start(service_name, command, args, service_file_path=str(service_file))
    updated_content = service_file.read()
    assert "ExecStart=/usr/bin/new_command --new-arg" in updated_content
    mock_reload.assert_called_once()
    mock_restart.assert_called_once_with(service_name, "restart")
    assert result is True


def test_set_system_service_exec_start_file_not_found(tmpdir):
    service_name = "nonexistent_service"
    command = "/usr/bin/new_command"
    with pytest.raises(FileNotFoundError):
        set_system_service_exec_start(
            service_name, command, service_file_path=str(tmpdir.join("nonexistent_file.service"))
        )
