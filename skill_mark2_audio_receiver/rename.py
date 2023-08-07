from typing import List, Optional
from skill_mark2_audio_receiver.systemd import set_system_service_exec_start, interact_with_service, reload_daemon
from skill_mark2_audio_receiver import read_file, write_to_file


def modify_key_value(content: List[str], key: str, value: str) -> List[str]:
    """
    Modify a key-value pair in a configuration content. If the key does not exist, it's appended.

    Args:
        content (List[str]): The content of the configuration file.
        key (str): The key to be modified.
        value (str): The value to set for the key.

    Returns:
        List[str]: The modified content.
    """
    key_found = False
    new_content = []
    for line in content:
        stripped = line.strip()
        if stripped.startswith(key):
            new_content.append(f"{key}={value}\n")
            key_found = True
        else:
            new_content.append(line)

    # Append the key if it doesn't exist
    if not key_found:
        new_content.append(f"{key}={value}\n")

    return new_content


def set_config_key_value(config_file_path: str, key: str, value: str) -> None:
    """
    Set a key-value pair in a configuration file.

    Args:
        config_file_path (str): The path to the configuration file.
        key (str): The key to be modified.
        value (str): The value to set for the key.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    content = read_file(config_file_path)
    updated_content = modify_key_value(content, key, value)
    write_to_file(config_file_path, updated_content)


def set_raspotify_device_name(name: str, config_path: str = "/etc/raspotify/conf") -> None:
    """
    Set the device name for Raspotify.

    Args:
        name (str): The name to be set for the Raspotify device.
        config_path (str, optional): The path to the Raspotify configuration file. Defaults to "/etc/raspotify/conf".
    """
    set_config_key_value(config_path, "LIBRESPOT_NAME", f'"{name}"')


def set_uxplay_device_name(name: str, service_file_path: Optional[str] = None) -> bool:
    """
    Set the device name for UxPlay.

    Args:
        name (str): The name to be set for the Raspotify device.
    Returns:
        bool: Whether or not the service was successfully restarted.
    """
    set_system_service_exec_start("uxplay", "/usr/bin/uxplay", f"-n '{name}'", service_file_path)
    # Reload the systemd daemon to recognize the changes
    reload_daemon()

    # Restarting the UxPlay service using the earlier mentioned systemd function.
    interact_with_service("uxplay", "restart")

    return True
