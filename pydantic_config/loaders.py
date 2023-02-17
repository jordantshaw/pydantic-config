import configparser
import json
import toml
import yaml


def json_file_loader(file: str, encoding: str = None):
    """ .json file type loader """
    with open(file, 'r', encoding=encoding) as file:
        return json.load(file)


def ini_file_loader(file: str, encoding: str = None):
    """ .ini file type loader """
    config = configparser.ConfigParser()
    config.read(file, encoding=encoding)
    return {k: dict(v) for k, v in config.items()}


def toml_file_loader(file: str, encoding: str = None):
    """ .toml file type loader """
    return toml.load(file)


def yaml_file_loader(file: str, encoding: str = None):
    """ .yaml file type loader """
    with open(file, 'r', encoding=encoding) as file:
        return yaml.safe_load(file)


