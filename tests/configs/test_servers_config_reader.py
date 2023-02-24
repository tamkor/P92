from pathlib import Path
from unittest.mock import patch

import pytest

from configs.servers_config_reader import ConfigReader


def test_config_reader_constructor_ok():
    ConfigReader()


@patch.object(ConfigReader, "CONFIG_FILE_PATH", new="not_valid/_file_path")
def test_config_reader_with_wrong_filepath():
    with pytest.raises(FileNotFoundError) as e:
        ConfigReader()
    assert str(e.value) == ConfigReader.FILE_NOT_FOUND_ERROR_MSG


@patch.object(ConfigReader, "CONFIG_FILE_PATH", new=Path(__file__).resolve().parent / "invalid.json")
def test_config_reader_with_invalid_json():
    with pytest.raises(ValueError) as e:
        ConfigReader()
    assert str(e.value) == ConfigReader.JSON_ERROR_MSG


@patch.object(ConfigReader, "CONFIG_FILE_PATH", new=Path(__file__).resolve().parent / "missing_key.json")
def test_config_reader_with_missing_key_in_json():
    with pytest.raises(KeyError) as e:
        ConfigReader()
    assert str(e.value) == f"'{ConfigReader.KEY_ERROR_MSG}'"
    # single quotes are required before and after the message, because Python is weird. Explained in the following
    # function: KeyError_str(PyBaseExceptionObject *self) at the source code of CPython's source code in this file:
    # https://github.com/python/cpython/blob/main/Objects/exceptions.c


