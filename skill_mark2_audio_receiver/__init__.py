from typing import List

from skill_mark2_audio_receiver.version import version

__version__ = version


def read_file(file_path: str) -> List[str]:
    """
    Read and return the content of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        List[str]: List of strings with each string being a line from the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()


def write_to_file(file_path: str, content: List[str]) -> None:
    """
    Write the updated content back to a file.

    Args:
        file_path (str): Path to the file.
        content (List[str]): List of strings to be written to the file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(content)
