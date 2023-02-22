from pydantic_config.loaders import toml_file_loader, ini_file_loader, yaml_file_loader, json_file_loader


def test_toml_load(config_toml_file):
    data = toml_file_loader(config_toml_file)
    assert data == {'app': {'description': 'description from config.toml'}}


def test_ini_load(config_ini_file):
    data = ini_file_loader(config_ini_file)
    assert data == {'DEFAULT': {}, 'APP': {'description': 'description from config.ini'}}


def test_yaml_load(config_yaml_file):
    data = yaml_file_loader(config_yaml_file)
    assert data == {'app': {'description': 'description from config.yaml'}}


def test_json_load(config_json_file):
    data = json_file_loader(config_json_file)
    assert data == {'app': {'description': 'description from config.json'}}
