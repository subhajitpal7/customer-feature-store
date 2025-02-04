import os
from pathlib import Path
import yaml

class ConfigManager:
    """Configuration management for the feature store"""
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from YAML file"""
        config_path = Path(__file__).parent / 'config.yaml'
        
        with open(config_path, 'r') as config_file:
            self._config = yaml.safe_load(config_file)
        
        project_root = str(Path(__file__).resolve().parents[3])
        for key, value in self._config.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, str):
                        self._config[key][subkey] = subvalue.format(project_root=project_root)
    
    def get_data_path(self, data_key: str) -> str:
        """Retrieve the full path for a given data key"""
        try:
            data_path = self._config['data'][data_key]
            return str(Path(data_path).resolve())
        except KeyError:
            raise KeyError(f"No data path configured for key: {data_key}")
    
    def get_config(self, *keys):
        """Retrieve nested configuration values"""
        config = self._config
        for key in keys:
            config = config[key]
        return config

config = ConfigManager()

def get_data_path(data_key: str) -> str:
    return config.get_data_path(data_key)
