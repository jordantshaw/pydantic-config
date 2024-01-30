# Contributing

## Clone the repository
Fork the repository on GitHub and clone your fork locally.

```shell
# Clone your fork and cd into the repo directory
git clone https://github.com/<your-username>/pydantic-config.git
cd pydantic-config
```

## Virtual environment
Create an isolated environment using python's built-in `venv` library. In this example we will create the 
virtual environment in the project root. 

```shell
# Create a virtual environment called "venv"
python -m venv venv

# Activate the virtual environment
source ./venv/bin/activate
```

## Install dependencies
Install the required dependencies using the command below. This will install all of the
project dependencies listed in the `pyproject.toml` file and also install the pydantic-config
package in editable mode.

```bash
# Install dependencies in the requirements.txt file
pip install -r requirements.txt
```

## Testing with pytest
After making your changes to the code, be sure to run all of the tests to make sure none of the changes
made have broken anything

```shell
pytest
```