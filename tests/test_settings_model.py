import pytest
from pydantic import BaseModel

from pydantic_config import SettingsModel, SettingsConfig


def test_config_file(config_toml_file):
    class App(BaseModel):
        name: str = 'AppName'
        description: str = None

    class Settings(SettingsModel):
        app: App

        model_config = SettingsConfig(
            config_file=[config_toml_file],
        )

    settings = Settings()
    assert settings.model_dump() == {'app': {'name': 'AppName', 'description': 'description from config.toml'}}


def test_case_sensitive_config(config_toml_file):
    class App(BaseModel):
        name: str = 'AppName'
        description: str = None

    class Settings(SettingsModel):
        APP: App = App()

        model_config = SettingsConfig(
            case_sensitive=True,
            extra='allow',
            config_file=[config_toml_file],
        )

    settings = Settings()
    assert settings.model_dump() == {
        'APP': {'name': 'AppName', 'description': None},
        'app': {'description': 'description from config.toml'}
    }


def test_case_insensitive_config(config_toml_file):
    class App(BaseModel):
        Name: str = 'AppName'
        description: str = None

    class Settings(SettingsModel):
        APP: App = App()

        model_config = SettingsConfig(
            case_sensitive=False,
            config_file=[config_toml_file],
        )

    settings = Settings()
    assert settings.model_dump() == {'APP': {'Name': 'AppName', 'description': 'description from config.toml'}}


def test_extra_config(config_toml_file):

    class Settings(SettingsModel):
        foo: str = 'bar'

        model_config = SettingsConfig(
            extra='allow',
            config_file=[config_toml_file],
        )

    settings = Settings()
    assert settings.model_dump() == {
        'foo': 'bar',
        'app': {'description': 'description from config.toml'}
    }


def test_invalid_config_file():
    file = 'invalid/file/path/file.toml'

    class Settings(SettingsModel):
        foo: str = 'bar'

        model_config = SettingsConfig(
            config_file=[file],
            config_file_required=True,
        )

    with pytest.raises(OSError) as exc:
        Settings()


def test_invalid_config_file_not_required():
    file = 'invalid/file/path/file.toml'

    class Settings(SettingsModel):
        foo: str = 'bar'

        model_config = SettingsConfig(
            config_file=[file],
            config_file_required=False,
        )

    settings = Settings()

    assert settings.model_dump() == {'foo': 'bar'}


def test_empty_config_file():
    class Settings(SettingsModel):
        foo: str = 'bar'

        model_config = SettingsConfig(
            config_file=[],
            config_file_required=True,
        )

    with pytest.raises(ValueError) as exc:
        Settings()


def test_config_merge_disabled(tmp_path):
    file_a = tmp_path / "a.toml"
    file_a.write_text('[app]\nname = "from file a"\ndescription = "from file a"')
    file_b = tmp_path / "b.toml"
    file_b.write_text('[app]\ndescription = "from file b"')

    class App(BaseModel):
        name: str = 'default'
        description: str = None

    class Settings(SettingsModel):
        app: App

        model_config = SettingsConfig(
            config_file=[str(file_a), str(file_b)],
            config_merge=False,
        )

    settings = Settings()
    # file b replaces file a entirely — name is not in file b so falls back to default
    assert settings.app.name == 'default'
    assert settings.app.description == 'from file b'


def test_multiple_config_files(config_toml_file, config_yaml_file):
    class App(BaseModel):
        name: str = 'AppName'
        description: str = None

    class Settings(SettingsModel):
        app: App

        model_config = SettingsConfig(
            config_file=[config_toml_file, config_yaml_file]
        )

    settings = Settings()
    assert settings.model_dump() == {'app': {'name': 'AppName', 'description': 'description from config.yaml'}}

