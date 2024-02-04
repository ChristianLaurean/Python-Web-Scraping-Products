import yaml
from pathlib import Path

def load_config():
    """
    Loads configuration from the 'config.yml' file in the current working directory.

    Returns:
        dict: Configuration data loaded from the file.
    """
    
    # Get the current working directory
    current_directory = Path.cwd()

    # Construct the path to the config file
    config_path = current_directory / 'config.yml'

    # Open and read the content of the config file
    with open(config_path, mode='r') as file:
        config_data = yaml.safe_load(file)

    return config_data