import configparser
import json
import sys


def json_file_reader(file: str, encoding: str = None):
    """ .json file type reader """
    with open(file, 'r', encoding=encoding) as fp:
        return json.load(fp)


def ini_file_reader(file: str, encoding: str = None):
    """ .ini file type reader """
    config = configparser.ConfigParser()
    config.read(file, encoding=encoding)
    return {k: dict(v) for k, v in config.items()}


def toml_file_reader(file: str, encoding: str = None):
    """ .toml file type reader """

    if sys.version_info >= (3, 11):
        import tomllib
    else:
        try:
            import tomli as tomllib
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "No module named 'tomli'. The 'tomli' package is required to load `.toml` files for python<3.11"
            )

    with open(file, mode="rb", encoding=encoding) as fp:
        return tomllib.load(fp)


def yaml_file_reader(file: str, encoding: str = None):
    """ .yaml file type reader """
    try:
        import yaml
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "No module named 'yaml'. The 'pyyaml' package is required to load `.yaml/yml` config files."
        )

    with open(file, 'r', encoding=encoding) as fp:
        return yaml.safe_load(fp)


