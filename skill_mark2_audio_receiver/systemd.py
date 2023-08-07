import os
import subprocess
from typing import List, Optional

from skill_mark2_audio_receiver import read_file, write_to_file


# TODO: Logging
def normalize_service_name(service_name: str) -> str:
    return f"{service_name}.service" if not service_name.endswith(".service") else service_name


def interact_with_service(service_name: str, command: str) -> bool:
    subprocess.run(["sudo", "systemctl", command, normalize_service_name(service_name)], check=True)
    return True


def get_service_status(service_name: str) -> bool:
    # Check needs to be false because services that aren't running return non-0 codes
    result = subprocess.call(["systemctl", "is-active", "--quiet", normalize_service_name(service_name)])
    return True if result == 0 else False


def reload_daemon():
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    return True


def modify_exec_start(content: List[str], command: str, args: Optional[str] = None) -> List[str]:
    """
    Modify the ExecStart line in a service's content.

    Args:
    - content (List[str]): The content of the service file.
    - command (str): The main command to be executed by ExecStart.
    - args (Optional[str]): Additional arguments for the command.

    Returns:
    - List[str]: The modified content.
    """

    exec_start_line = f"ExecStart={command}"
    if args:
        exec_start_line += f" {args}"

    return [f"{exec_start_line}\n" if line.startswith("ExecStart=") else line for line in content]


def set_system_service_exec_start(
    service_name: str, command: str, args: Optional[str] = None, service_file_path: Optional[str] = None
) -> bool:
    """
    Set the ExecStart command in a systemd service file.

    Args:
    - service_name (str): The name of the service.
    - command (str): The main command to be executed by ExecStart.
    - args (Optional[str]): Additional arguments for the command.
    - service_file_path (Optional[str]): Path to the systemd service file.

    Returns:
    - bool: True if the command was successfully set, False otherwise.
    """

    if not service_file_path:
        service_file_path = f"/usr/lib/systemd/system/{service_name}.service"

    if not os.path.exists(service_file_path):
        raise FileNotFoundError(f"Service file {service_file_path} not found.")

    content = read_file(service_file_path)
    updated_content = modify_exec_start(content, command, args)
    write_to_file(service_file_path, updated_content)

    # Reload the systemd daemon to recognize the changes
    reload_daemon()

    # Restarting the service
    interact_with_service(service_name, "restart")

    return True
