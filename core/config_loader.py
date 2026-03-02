import yaml


def load_config(config_path: str) -> dict:
    """
    Load configuration settings from YAML file.

    Parameters:
    config_path (str): Path to YAML config file

    Returns:
    dict: Configuration dictionary
    """

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config
