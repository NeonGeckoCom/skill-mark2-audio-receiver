import subprocess
import time
from skill_mark2_audio_receiver.systemd import interact_with_service


def auto_pair_bluetooth() -> None:
    subprocess.run("/usr/local/bin/bluetooth-agent.sh", check=True)


def auto_pair_kdeconnect(timeout: int = 30) -> None:
    interact_with_service("pair-kdeconnect", "start")
    time.sleep(timeout)
    interact_with_service("pair-kdeconnect", "stop")
