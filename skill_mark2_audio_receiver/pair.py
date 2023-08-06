import subprocess
import time

from tenacity import retry, stop_after_delay, wait_fixed


def fetch_kdeconnect_devices() -> list[str]:
    output = subprocess.check_output("kdeconnect-cli -l", shell=True, text=True)
    return output.split("\n")


def extract_unpaired_device_ids(device_list: list[str]) -> list[str]:
    unpaired_ids = []
    for line in device_list:
        if "reachable" in line and "paired" not in line:
            device_id = line.split(":")[1].split("(")[0].strip()
            unpaired_ids.append(device_id)
    return unpaired_ids


def pair_kde_device(device_id: str) -> None:
    subprocess.run(f"kdeconnect-cli --pair -d {device_id}", shell=True, check=True)


def load_pulseaudio_bluetooth_modules() -> None:
    subprocess.run(["pactl", "load-module", "module-bluetooth-discover"], check=False)
    subprocess.run(["pactl", "load-module", "module-bluetooth-policy"], check=False)


def configure_pulseaudio_tcp() -> None:
    cmd = "load-module module-native-protocol-tcp auth-ip-acl=0.0.0.0/0 auth-anonymous=1"
    subprocess.run(["pacmd"], input=cmd.encode("utf-8"), check=True)


def set_bluetoothctl_pairing_mode(mode: str = "on") -> None:
    commands = ["agent on", "default-agent", f"pairable {mode}"]
    subprocess.run(["bluetoothctl"], input="\n".join(commands).encode("utf-8"), check=True)


def unload_pulseaudio_bluetooth_modules() -> None:
    subprocess.run(["pactl", "unload-module", "module-bluetooth-discover"], check=False)
    subprocess.run(["pactl", "unload-module", "module-bluetooth-policy"], check=False)


def reset_pulseaudio_tcp_module() -> None:
    cmd = "unload-module module-native-protocol-tcp"
    subprocess.run(["pacmd"], input=cmd.encode("utf-8"), check=True)


# Auto-pairing functions
@retry(
    stop=stop_after_delay(30), wait=wait_fixed(5)
)  # Retry for up to 30 seconds with a 5-second wait between retries
def auto_pair_kde_devices() -> None:
    start_time = time.time()
    while time.time() - start_time < 30:
        device_list = fetch_kdeconnect_devices()
        unpaired_ids = extract_unpaired_device_ids(device_list)
        for device_id in unpaired_ids:
            pair_kde_device(device_id)
            print(f"Paired with device ID: {device_id}")
        time.sleep(5)  # Wait for 5 seconds before trying again


def auto_pair_bluetooth() -> None:
    # Setup
    load_pulseaudio_bluetooth_modules()
    configure_pulseaudio_tcp()
    set_bluetoothctl_pairing_mode(mode="on")

    # Wait for 30 seconds to give the user time to prepare the pairing
    time.sleep(30)

    # Teardown
    set_bluetoothctl_pairing_mode(mode="off")
    unload_pulseaudio_bluetooth_modules()
    # Reset PulseAudio TCP module
    reset_pulseaudio_tcp_module()
