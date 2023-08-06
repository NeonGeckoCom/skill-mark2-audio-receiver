# pylint: disable=missing-function-docstring
import pytest

# Import the functions from the module
from skill_mark2_audio_receiver.rename import (
    read_file,
    write_to_file,
    modify_key_value,
    set_config_key_value,
    set_raspotify_device_name,
)


def test_read_file(tmpdir):
    # Create a temporary file with some content
    file_path = tmpdir.join("test_file.txt")
    file_path.write("line1\nline2\n")

    content = read_file(file_path.strpath)
    assert content == ["line1\n", "line2\n"]


def test_write_to_file(tmpdir):
    content = ["line1\n", "line2\n"]
    file_path = tmpdir.join("test_file.txt")
    write_to_file(file_path.strpath, content)

    with open(file_path.strpath, "r", encoding="utf-8") as f:
        assert f.readlines() == content


def test_set_config_key_value(tmpdir):
    file_path = tmpdir.join("config.conf")
    file_path.write("key1=value1\nkey2=value2\n")

    set_config_key_value(file_path.strpath, "key1", "new_value1")
    with open(file_path.strpath, "r", encoding="utf-8") as f:
        content = f.readlines()
        assert content == ["key1=new_value1\n", "key2=value2\n"]

    set_config_key_value(file_path.strpath, "key3", "value3")
    with open(file_path.strpath, "r", encoding="utf-8") as f:
        content = f.readlines()
        assert content == ["key1=new_value1\n", "key2=value2\n", "key3=value3\n"]


def test_set_raspotify_device_name(tmpdir):
    file_path = tmpdir.join("raspotify.conf")
    file_path.write('DEVICE_NAME="Old Name"\n')

    set_raspotify_device_name("New Name", file_path.strpath)

    with open(file_path.strpath, "r", encoding="utf-8") as f:
        content = f.readlines()
        assert content == ['DEVICE_NAME="New Name"\n']


# Test the modification of a key-value pair in a given content
def test_modify_key_value():
    content = ["key1=value1\n", "key2=value2\n"]
    updated_content = modify_key_value(content, "key1", "new_value1")
    assert updated_content == ["key1=new_value1\n", "key2=value2\n"]

    updated_content2 = modify_key_value(content, "key3", "value3")
    assert updated_content2 == ["key1=value1\n", "key2=value2\n", "key3=value3\n"]


# Test exceptions raised for invalid config paths
@pytest.mark.parametrize(
    "config_path, key, value, expected_exception",
    [
        (None, "key1", "value1", TypeError),
        ("/nonexistentpath", "key1", "value1", FileNotFoundError),
    ],
)
def test_set_config_key_value_exceptions(config_path, key, value, expected_exception):
    with pytest.raises(expected_exception):
        set_config_key_value(config_path, key, value)
