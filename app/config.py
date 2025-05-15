import yaml
from pathlib import Path

CONFIG_PATH = "conf/config.yaml"

def load_config():
    config_path = Path(__file__).parent.parent / CONFIG_PATH
    with open(config_path, "r") as config_file:
        return yaml.safe_load(config_file)

config = load_config()
