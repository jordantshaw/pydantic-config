import pytest
from pydantic import BaseModel

from pydantic_config import SettingsModel


def test_config_file(config_toml_file):
    class App(BaseModel):
        name: str = 'AppName'
        description: str = None

    class Settings(SettingsModel):
        app: App

        class Config:
            config_file = [config_toml_file]

    settings = Settings()
    assert settings.dict() == {'app': {'name': 'AppName', 'description': 'description from config.toml'}}


def test_invalid_config_file():
    file = 'invalid/file/path/file.toml'

    class Settings(SettingsModel):
        foo: str = 'bar'

        class Config:
            config_file = [file]

    with pytest.raises(OSError) as exc:
        Settings()


def test_multiple_config_files(config_toml_file, config_yaml_file):
    class App(BaseModel):
        name: str = 'AppName'
        description: str = None

    class Settings(SettingsModel):
        app: App

        class Config:
            config_file = [config_toml_file, config_yaml_file]

    settings = Settings()
    assert settings.dict() == {'app': {'name': 'AppName', 'description': 'description from config.yaml'}}

