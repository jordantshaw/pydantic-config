from copy import deepcopy
from pathlib import Path
from typing import Dict, Any, Union, List

from pydantic import BaseSettings, BaseModel

from .loaders import (
    ini_file_loader,
    toml_file_loader,
    yaml_file_loader,
    json_file_loader
)


class SettingsModel (BaseSettings):

    class Config:

        config_files: List = []
        config_file_encoding: str = None
        config_merge: bool = True
        config_merge_unique: bool = True

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
                config_file_settings,
            )



def config_file_settings(settings: BaseSettings) -> Dict[str, Any]:
    encoding = getattr(settings.__config__, 'config_file_encoding', None)
    files = getattr(settings.__config__, 'config_file', [])
    config_merge = getattr(settings.__config__, 'config_merge', True)
    config_merge_unique = getattr(settings.__config__, 'config_merge_unique', True)

    if isinstance(files, str):
        files = [files]

    config = {}
    for file in files:
        if config_merge:
            config = _deep_merge(
                base=config,
                nxt=_load_config_file(file, encoding),
                unique=config_merge_unique,
            )
        else:
            config.update(_load_config_file(file, encoding))

    return config


def _deep_merge(base: dict, nxt: dict, unique: bool = True) -> dict:
    """
    Merges nested dictionaries.

    Parameters
    ----------
    base: dict
        The base dictionary to merge into
    nxt: dict
        The dictionary to merge into base
    unique: bool
        This determines the behavior when merging list values. Lists are appended together which could result
        in duplicate values.  To avoid duplicates set this value to True.

    """
    result = deepcopy(base)

    for key, value in nxt.items():
        if isinstance(result.get(key), dict) and isinstance(value, dict):
            result[key] = _deep_merge(result.get(key), value)
        elif isinstance(result.get(key), list) and isinstance(value, list):
            if unique:
                result[key] = result.get(key) + [i for i in deepcopy(value) if i not in set(result.get(key))]
            else:
                result[key] = result.get(key) + deepcopy(value)
        else:
            result[key] = deepcopy(value)
    return result


def _load_config_file(file: str, encoding: str) -> Dict[str, Any]:
    """ Loads config file with selected encoding """
    file = Path(file)
    if not file.exists():
        raise OSError(f"Could not load file from provided config file: {file}")

    file_loaders = {
        '.ini': ini_file_loader,
        '.toml': toml_file_loader,
        '.yaml': yaml_file_loader,
        '.json': json_file_loader,
    }

    return file_loaders.get(file.suffix)(str(file), encoding)

