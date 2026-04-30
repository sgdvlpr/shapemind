import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".shapemind"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "calendar": "persian",
    "date_format": "%Y-%m-%d"
}

def get_config():
    """Load user configuration"""
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    
def set_config(key, vlalue):
    """Update configuration"""
    config = get_config()
    config[key] = vlalue
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)