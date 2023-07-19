import configparser
import json


def json_file_reader(file: str, encoding: str = None):
    """ .json file type reader """
    with open(file, 'r', encoding=encoding) as file:
        return json.load(file)


def ini_file_reader(file: str, encoding: str = None):
    """ .ini file type reader """
    config = configparser.ConfigParser()
    config.read(file, encoding=encoding)
    return {k: dict(v) for k, v in config.items()}


def toml_file_reader(file: str, encoding: str = None):
    """ .toml file type reader """
    try:
        import toml
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "No module named 'toml'. The 'toml' package is required when loading `.toml` config files."
        )

    return toml.load(file)


def yaml_file_reader(file: str, encoding: str = None):
    """ .yaml file type reader """
    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "No module named 'yaml'. The 'pyyaml' package is required when loading `.yaml/yml` config files."
        )

    with open(file, 'r', encoding=encoding) as file:
        return yaml.safe_load(file)


