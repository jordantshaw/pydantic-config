# Pydantic Config
Support for Pydantic settings configuration file loading

## Installation
`pip install pydantic-config`

## Usage

```toml
# config.toml
app_name = "Python Application"
description = "Test application description"
```

```python
from pydantic_config import SettingsModel


class Settings(SettingsModel):
    app_id: str = 1
    app_name: str = None
    description: str = None
    log_level: str = 'INFO'

    class Config:
        config_file = 'config.toml'


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
from pydantic_config import SettingsModel


class Settings(SettingsModel):
    app_id: str = 1
    app_name: str = 'App Name'
    description: str = None
    log_level: str = 'INFO'

    class Config:
        config_file = ['config.toml', 'config.json']  # The config.json file will take priority over config.toml


settings = Settings()
print(settings)
# app_id='1' app_name='Python Application' description='Description from JSON file' log_level='WARNING'
```


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
from pydantic_config import SettingsModel


class Settings(SettingsModel):
    foo: dict = {}

    class Config:
        config_file = ['config.toml', 'config2.toml']
        config_merge: bool = True


settings = Settings()
print(settings)
# foo={'item1': 'value1', 'item2': 'value2'}

# If config_merge=False then config2.toml would ovverride the values from config.toml
# foo={'item2': 'value2'}
```

## Duplicate items in merged lists
By default, only unique `list` items will be merged. To disable this behavior and keep all items
of a `list` regardless of duplication set the `config_merge_unique` option to `False`. 


