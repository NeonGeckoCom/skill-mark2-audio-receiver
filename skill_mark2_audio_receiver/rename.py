def read_file(file_path: str) -> list[str]:
    """
    Read and return the content of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        list[str]: List of strings with each string being a line from the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()


def write_to_file(file_path: str, content: list[str]) -> None:
    """
    Write the updated content back to a file.

    Args:
        file_path (str): Path to the file.
        content (list[str]): List of strings to be written to the file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(content)


def modify_key_value(content: list[str], key: str, value: str) -> list[str]:
    """
    Modify a key-value pair in a configuration content. If the key does not exist, it's appended.

    Args:
        content (list[str]): The content of the configuration file.
        key (str): The key to be modified.
        value (str): The value to set for the key.

    Returns:
        list[str]: The modified content.
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
    set_config_key_value(config_path, "DEVICE_NAME", f'"{name}"')
