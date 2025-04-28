# Pydantic Config
Pydantic Config extends Pydantic’s BaseSettings to support loading configuration from files like 
JSON, INI, TOML, and YAML — in addition to environment variables.

[![PyPI](https://img.shields.io/pypi/v/pydantic-config.svg)](https://pypi.org/project/pydantic-config/)
[![Conda](https://img.shields.io/conda/vn/conda-forge/pydantic-config.svg)](https://anaconda.org/conda-forge/pydantic-config)
[![License](https://img.shields.io/github/license/jordantshaw/pydantic-config)](https://github.com/jordantshaw/pydantic-config/blob/main/LICENSE)

---

## Table of Contents

- [Why Pydantic Config?](#why-pydantic-config)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Loading Multiple Config Files](#loading-multiple-config-files)
- [Supported File Formats](#supported-file-formats)
- [Using `.env` Files](#using-env-files)
- [Requiring Config Files to Exist](#requiring-config-files-to-exist)
- [Merging](#merging)
- [Handling Duplicates in Merged Lists](#handling-duplicates-in-merged-lists)
- [License](#license)

---

## Why Pydantic Config?
✅ Load settings from `.json`, `.ini`, `.toml`, `.yaml`, and `.env` files.  
✅ Support for multiple files with override/merge strategies.  
✅ Compatible with Pydantic v2 `BaseSettings`.  
✅ Lightweight and simple integration.

---

## Installation
Install with pip:
```bash
pip install pydantic-config
```

Or with conda (via the conda-forge channel):
```bash
conda install pydantic-config -c conda-forge
```

### Optional Dependencies
To enable additional file formats, you can install optional dependencies:

| Format | Install Command |
|:-------|:----------------|
| YAML   | `pip install pydantic-config[yaml]` |
| TOML (for Python < 3.11) | `pip install pydantic-config[toml]` |

To install **all** optional dependencies:

```bash
pip install pydantic-config[all]
```

---

## Quick Start

Load settings from a config file:

**config.toml**
```toml
app_name = "Python Application"
description = "Test application description"
```

**settings.py**
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

---

## Loading Multiple Config Files
Multiple config files can be loaded by passing a `list` of file names. Files will be loaded in the order they are listed.
Meaning later files in the `list` will take priority over earlier files.

**config.toml**
```toml
app_name = "Python Application"
description = "Test application description"
```

**config.json**
```json
{
  "description": "Description from JSON file",
  "log_level": "WARNING"
}
```

**settings.py**
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

---

## Supported File Formats
Currently, the following file formats are supported:
  - `.yaml` _Requires `pyyaml` package_
  - `.toml` _Requires `tomli` package for python<3.11_
  - `.json`
  - `.ini`

---

## Using `.env` files
Since Pydantic natively supports dotenv files, you can combine a `.env` file with config files easily.  
Values from the `.env` file **take precedence** over config files.

```python
from pydantic_config import SettingsModel, SettingsConfig

class Settings(SettingsModel):
  app_name: str = None
  description: str = None
    
    model_config = SettingsConfig(
        env_file='.env',
        config_file='config.toml',
    )
```

---

## Requiring Config Files to Exist
By default, missing config files are ignored (no error is raised). This may be useful if you want to specify 
config files that may not always exist. For example, you might have different config files for per 
environment: `config-prod.toml` and `config-dev.toml`.

To enforce that config files must exist, set `config_file_required=True`. This will cause an error to be raised
if the specified config file(s) does not exist. 

```python
model_config = SettingsConfig(
    config_file='config.toml',
    config_file_required=True,
)
```

⚠️ When `config_file_required=True`, `config_file` cannot be `None` or an empty list `[]`.

---

## Merging
By default, when merging multiple config files:
- `dict` values are **merged** (keys combined).
- `list` values are **merged** (items combined).

To disable merging and prefer overwriting entirely, set `config_merge=False`.

**Example:**

**config.toml**
```toml
[foo]
item1 = "value1"
```

**config2.toml**
```toml
[foo]
item2 = "value2"
```

**settings.py**
```python
from pydantic_config import SettingsModel, SettingsConfig

class Settings(SettingsModel):
    foo: dict = {}

    model_config = SettingsConfig(
        config_file=['config.toml', 'config2.toml'],
        config_merge=True,
    )

settings = Settings()
print(settings)
# foo={'item1': 'value1', 'item2': 'value2'}
```

If `config_merge=False`, the second file would **overwrite** the first:

```text
foo={'item2': 'value2'}
```

---

## Handling Duplicates in Merged Lists
By default, merged lists **include all items**, even duplicates.

To ensure list items are **unique** during merge, set `config_merge_unique=True`.

```python
model_config = SettingsConfig(
    config_file=['config1.toml', 'config2.toml'],
    config_merge=True,
    config_merge_unique=True,
)
```


## License
This project is licensed under the [MIT License](https://github.com/jordantshaw/pydantic-config/blob/main/LICENSE).



