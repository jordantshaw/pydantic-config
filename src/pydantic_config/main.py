import os
from pathlib import Path
from typing import Dict, Any, Union, List, Type, Tuple, Mapping

from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from pydantic_settings.sources import PydanticBaseEnvSettingsSource

from .merge import deep_merge
from .readers import (
    ini_file_reader,
    toml_file_reader,
    yaml_file_reader,
    json_file_reader
)


ConfigFileType = Union[Path, str, List[Union[Path, str]], Tuple[Union[Path, str], ...]]


class SettingsError(ValueError):
    pass


class SettingsConfig(SettingsConfigDict, total=False):
    config_file: Union[ConfigFileType, None]
    config_file_encoding: Union[str, None]
    config_merge: bool
    config_merge_unique: bool


class SettingsModel(BaseSettings):

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            ConfigFileSettingsSource(settings_cls),
        )


class ConfigFileSettingsSource(PydanticBaseEnvSettingsSource):
    """ Settings source class that loads values from one more configuration files. """
    def __init__(
            self,
            settings_cls: Type[BaseSettings],
            case_sensitive: Union[bool, None] = None,
            config_file: Union[ConfigFileType, None] = None,
            config_file_encoding: Union[str, None] = None,
            config_merge: bool = True,
            config_merge_unique: bool = True,

    ) -> None:
        super().__init__(settings_cls, case_sensitive)
        self.config: SettingsConfig
        self.config_file = config_file or self.config.get('config_file', None)
        self.config_file_encoding = config_file_encoding or self.config.get('config_file_encoding', None)
        self.config_merge = config_merge or self.config.get('config_merge', True)
        self.config_merge_unique = config_merge_unique or self.config.get('config_merge_unique', True)
        self.config_values = self._load_config_values()

    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
        config_val: Any = self.config_values.get(field_name)
        return config_val, field_name, False

    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        if value is None:
            value = self.config_values.get(field_name if self.case_sensitive else field_name.lower())
            if value:
                return value

        return value

    def _lowercase_dict_keys(self, d: Dict):
        return {k.lower(): self._lowercase_dict_keys(v) if isinstance(v, dict) else v for k, v in d.items()}

    def _load_config_values(self) -> Dict[str, Any]:
        """ Gets the config values from the configuration files """
        config_values = self._read_config_files()
        if self.case_sensitive:
            return config_values

        return self._lowercase_dict_keys(config_values)

    def _read_config_files(self) -> Dict[str, Any]:
        """ Reads config files and merges config values if merging is enabled """
        config_files = self.config_file
        if config_files is None:
            return {}

        if isinstance(config_files, (str, os.PathLike)):
            config_files = [config_files]

        config = {}
        for file in config_files:
            file_path = Path(file).expanduser()
            if not file_path.exists():
                raise OSError(f"Config file `{file}` not found")

            if self.config_merge:
                config = deep_merge(
                    base=config,
                    nxt=self._read_config_file(file_path),
                    unique=self.config_merge_unique,
                )
            else:
                config.update(self._read_config_file(file_path))
        return config

    def _read_config_file(self, file: Path) -> Dict[str, Any]:
        """ Reads single config file based on file extension """
        file_loaders = {
            '.ini': ini_file_reader,
            '.toml': toml_file_reader,
            '.yaml': yaml_file_reader,
            '.json': json_file_reader,
        }

        return file_loaders.get(file.suffix)(str(file), self.config_file_encoding)

    def __call__(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().__call__()

        data_lower_keys: List[str] = []
        if not self.case_sensitive:
            data_lower_keys = [x.lower() for x in data.keys()]

        # As `extra` config is allowed in config settings source, We have to
        # update data with extra config values from the config files.
        for config_name, config_value in self.config_values.items():
            if config_value is not None:
                if (data_lower_keys and config_name not in data_lower_keys) or (
                        not data_lower_keys and config_name not in data):
                    data[config_name] = config_value

        return data
