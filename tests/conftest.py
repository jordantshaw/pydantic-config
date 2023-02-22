from datetime import timedelta
from typing import Generator, Any

import pytest


@pytest.fixture(scope='session')
def config_toml_file(tmp_path_factory):
    config = '''
    [app]
    description = "description from config.toml"
    '''
    file_path = tmp_path_factory.mktemp("data") / "config.toml"
    with open(file_path, 'w') as file:
        file.write(config)

    return file_path


@pytest.fixture(scope='session')
def config_yaml_file(tmp_path_factory):
    config = '''
    app:
        description: description from config.yaml
    '''
    file_path = tmp_path_factory.mktemp("data") / "config.yaml"
    with open(file_path, 'w') as file:
        file.write(config)

    return file_path


@pytest.fixture(scope='session')
def config_ini_file(tmp_path_factory):
    config = '''
    [APP]
    DESCRIPTION = description from config.ini
    '''
    file_path = tmp_path_factory.mktemp("data") / "config.ini"
    with open(file_path, 'w') as file:
        file.write(config)

    return file_path


@pytest.fixture(scope='session')
def config_json_file(tmp_path_factory):
    config = '''
    {
        "app": {
            "description": "description from config.json"
        }
    }
    '''
    file_path = tmp_path_factory.mktemp("data") / "config.json"
    with open(file_path, 'w') as file:
        file.write(config)

    return file_path

