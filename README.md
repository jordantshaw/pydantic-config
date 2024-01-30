# Pydantic Config
Support for Pydantic settings configuration file loading

## Installation
Pydantic Config can be installed via pip:

`pip install pydantic-config`

Pydantic Config is also available on conda under the conda-forge channel:

`conda install pydantic-config -c conda-forge`



### Optional Dependencies

Pydantic-Config has the following optional dependencies:
  - yaml - `pip install pydantic-config[yaml]`
  - toml - `pip install pydantic-config[toml]` _Only for python<3.11_

You can install all the optional dependencies with `pip install pydantic-config[all]`

## Usage

```toml
# config.toml
app_name = "Python Application"
description = "Test application description"
```

```python
from pydantic_config import SettingsModel, SettingsConfig


class Settings(SettingsModel):
    app_id: str = 1
    app_name: str = None
    description: str = None
    log_level: str = 'INFO'
    
    model_config = SettingsConfig(
        config_file='config.toml',
    )


settings = Settings()
print(settings)
# app_id='1' app_name='Python Application' description='Test application description' log_level='INFO'

```

## Using multiple config files
Multiple config files can be loaded by passing a `list` of file names. Files will be loaded in the order they are listed.
Meaning later files in the `list` will take priority over earlier files.

```toml
# config.toml
app_name = "Python Application"
description = "Test application description"
```


```json
// config.json
{
  "description": "Description from JSON file",
  "log_level": "WARNING"
}
```

```python
from pydantic_config import SettingsModel, SettingsConfig


class Settings(SettingsModel):
    app_id: str = 1
    app_name: str = 'App Name'
    description: str = None
    log_level: str = 'INFO'
    
    model_config = SettingsConfig(
        config_file=['config.toml', 'config.json']  # The config.json file will take priority over config.toml
    )

settings = Settings()
print(settings)
# app_id='1' app_name='Python Application' description='Description from JSON file' log_level='WARNING'
```

## Supported file formats
Currently, the following file formats are supported:
  - `.yaml` _Requires `pyyaml` package_
  - `.toml` _Requires `tomli` package for python<3.11_
  - `.json`
  - `.ini`

## Using dotenv files
`pydantic-config` supports using dotenv files because `pydantic-settings` natively supports dotenv files. 
To use a dotenv file in conjunction with the config files simply set `env_file` parameter in `SettingsConfig`.
The values in the dotenv file will take precedence over the values in the config files.

```python
class Settings(SettingsModel):
  app_name: str = None
  description: str = None
    
    model_config = SettingsConfig(
        env_file='.env',
        config_file='config.toml',
    )
```


## Requiring config files to load
Config files will attempt to be loaded from the specified file path. By default, if no file is found the file 
will simply not be loaded (no error occurs). This may be useful if you want to specify config files that 
may or may not exist. For example, you may have different config files for per 
environment: `config-prod.toml` and `config-dev.toml`.

To disable this behavior set `config_file_required=True`. This will cause an error to be raised
if the specified config file(s) do not exist. Setting this to `True` will also prohibit the `config_file`
parameter from being set to `None` or empty `[]`.


## Merging
If your configurations have existing `list` or `dict` variables the contents will be merged by default. To disable
this behavior and override the contents instead you can set the `config_merge` option to `False` in the settings 
`Config` class.

```toml
# config.toml
[foo]
item1 = "value1"
```
```toml
# config2.toml
[foo]
item2 = "value2"
```

```python
from pydantic_config import SettingsModel, SettingsConfig


class Settings(SettingsModel):
    foo: dict = {}
    
    model_config = SettingsConfig(
        config_file=['config.toml', 'config2.toml'],
        config_merge= True,
    )


settings = Settings()
print(settings)
# foo={'item1': 'value1', 'item2': 'value2'}

# If config_merge=False then config2.toml would override the values from config.toml
# foo={'item2': 'value2'}
```

## Duplicate items in merged lists
By default, __all__ `list` items will be merged into a single list regardless of duplicated items. To only keep
unique list items, set `config_merge_unique=True`. This will only keep unique items in within a list.


