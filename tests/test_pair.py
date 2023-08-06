# pylint: disable=missing-function-docstring
from unittest.mock import patch, call

import pytest

from skill_mark2_audio_receiver.pair import (
    auto_pair_bluetooth,
    auto_pair_kde_devices,
    load_pulseaudio_bluetooth_modules,
    configure_pulseaudio_tcp,
    set_bluetoothctl_pairing_mode,
    unload_pulseaudio_bluetooth_modules,
    reset_pulseaudio_tcp_module,
    extract_unpaired_device_ids,
    fetch_kdeconnect_devices,
    pair_kde_device,
)


# Test fetch_kdeconnect_devices function
def test_fetch_kdeconnect_devices():
    with patch("subprocess.check_output") as mock_check_output:
        mock_output = """- Device A: id_12345 (paired and reachable)
- Device B: id_67890 (paired)
- Device C: id_11223 (paired and reachable)
- Device D: id_45678 (reachable)
4 devices found"""
        mock_check_output.return_value = mock_output

        devices = fetch_kdeconnect_devices()
        assert devices == [
            "- Device A: id_12345 (paired and reachable)",
            "- Device B: id_67890 (paired)",
            "- Device C: id_11223 (paired and reachable)",
            "- Device D: id_45678 (reachable)",
            "4 devices found",
        ]


# Test extract_unpaired_device_ids function
@pytest.mark.parametrize(
    "device_list,expected",
    [
        (
            [
                "- Device A: id_12345 (paired and reachable)",
                "- Device B: id_67890 (paired)",
                "- Device C: id_11223 (paired and reachable)",
                "- Device D: id_45678 (reachable)",
            ],
            ["id_45678"],
        ),
        (["- Device E: id_89101 (paired and reachable)"], []),
        ([], []),
    ],
)
def test_extract_unpaired_device_ids(device_list, expected):
    assert extract_unpaired_device_ids(device_list) == expected


# Test pair_device function
def test_pair_kde_device():
    with patch("subprocess.run") as mock_run:
        pair_kde_device("12345")
        mock_run.assert_called_once_with("kdeconnect-cli --pair -d 12345", shell=True, check=True)


# Bluetooth


def test_load_pulseaudio_bluetooth_modules():
    with patch("subprocess.run") as mock_run:
        load_pulseaudio_bluetooth_modules()
        calls = [
            call(["pactl", "load-module", "module-bluetooth-discover"], check=False),
            call(["pactl", "load-module", "module-bluetooth-policy"], check=False),
        ]
        mock_run.assert_has_calls(calls)


def test_configure_pulseaudio_tcp():
    with patch("subprocess.run") as mock_run:
        configure_pulseaudio_tcp()
        cmd = "load-module module-native-protocol-tcp auth-ip-acl=0.0.0.0/0 auth-anonymous=1"
        mock_run.assert_called_once_with(["pacmd"], input=cmd.encode("utf-8"), check=True)


def test_set_bluetoothctl_pairing_mode():
    with patch("subprocess.run") as mock_run:
        set_bluetoothctl_pairing_mode()
        commands = ["agent on", "default-agent", "pairable on"]
        mock_run.assert_called_once_with(["bluetoothctl"], input="\n".join(commands).encode("utf-8"), check=True)


def test_unload_pulseaudio_bluetooth_modules():
    with patch("subprocess.run") as mock_run:
        unload_pulseaudio_bluetooth_modules()
        calls = [
            call(["pactl", "unload-module", "module-bluetooth-discover"], check=False),
            call(["pactl", "unload-module", "module-bluetooth-policy"], check=False),
        ]
        mock_run.assert_has_calls(calls)


def test_reset_pulseaudio_tcp_module():
    with patch("subprocess.run") as mock_run:
        reset_pulseaudio_tcp_module()
        cmd = "unload-module module-native-protocol-tcp"
        mock_run.assert_called_once_with(["pacmd"], input=cmd.encode("utf-8"), check=True)


@patch("time.time", side_effect=[0, 0, 31, 31])  # Simulate 31 seconds passing between two calls
@patch("time.sleep")
@patch("skill_mark2_audio_receiver.pair.pair_kde_device")
@patch("skill_mark2_audio_receiver.pair.extract_unpaired_device_ids")
@patch("skill_mark2_audio_receiver.pair.fetch_kdeconnect_devices")
def test_auto_pair_kde_devices(mock_fetch, mock_extract, mock_pair, mock_sleep, mock_time):
    # Simulate two devices being found, one of which is unpaired
    mock_fetch.return_value = ["device1", "device2"]
    mock_extract.return_value = ["device2"]

    auto_pair_kde_devices()

    # Check that the pair function was called for the unpaired device
    mock_pair.assert_called_with("device2")


@patch("time.time", side_effect=[0, 31])  # Simulate 31 seconds passing between two calls
@patch("time.sleep")
@patch("skill_mark2_audio_receiver.pair.set_bluetoothctl_pairing_mode")
@patch("skill_mark2_audio_receiver.pair.configure_pulseaudio_tcp")
@patch("skill_mark2_audio_receiver.pair.load_pulseaudio_bluetooth_modules")
@patch("skill_mark2_audio_receiver.pair.reset_pulseaudio_tcp_module")
@patch("skill_mark2_audio_receiver.pair.unload_pulseaudio_bluetooth_modules")
def test_auto_pair_bluetooth(mock_unload, mock_reset, mock_load, mock_configure, mock_set_mode, mock_sleep, mock_time):
    auto_pair_bluetooth()

    # Check the order of function calls
    mock_load.assert_called()
    mock_configure.assert_called()
    mock_set_mode.assert_has_calls([call(mode="on"), call(mode="off")])  # Check both calls
    mock_unload.assert_called()
    mock_reset.assert_called()
