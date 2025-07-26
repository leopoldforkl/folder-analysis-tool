import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Manages configuration settings for the folder analysis tool"""
    
    DEFAULT_CONFIG = {
        "input_directory": ".",
        "output_directory": "./output",
        "include_hidden_files": False,
        "include_pycache": False,
        "output_to_console": True,
        "output_to_file": True,
        "output_filename": "folder_structure.txt",
        "include_file_contents": []
    }
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the configuration manager
        
        Args:
            config_path (str): Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default if it doesn't exist
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                merged_config = self.DEFAULT_CONFIG.copy()
                merged_config.update(config)
                return merged_config
                
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Warning: Could not load config file {self.config_path}: {e}")
                print("Using default configuration.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict[str, Any] = None) -> None:
        """
        Save configuration to file
        
        Args:
            config (Dict[str, Any], optional): Configuration to save. If None, saves current config.
        """
        config_to_save = config if config is not None else self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save config file {self.config_path}: {e}")
    
    def get(self, key: str, default=None) -> Any:
        """
        Get a configuration value
        
        Args:
            key (str): Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Any: Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value
        
        Args:
            key (str): Configuration key
            value (Any): Value to set
        """
        self.config[key] = value
    
    def update_from_args(self, input_dir: str = None, output_dir: str = None) -> None:
        """
        Update configuration from command line arguments
        
        Args:
            input_dir (str, optional): Input directory from command line
            output_dir (str, optional): Output directory from command line
        """
        if input_dir is not None:
            self.set("input_directory", input_dir)
        
        if output_dir is not None:
            self.set("output_directory", output_dir)
            self.set("output_to_file", True)
    
    def should_include_file(self, file_path: Path) -> bool:
        """
        Determine if a file should be included based on configuration
        
        Args:
            file_path (Path): Path to the file to check
            
        Returns:
            bool: True if file should be included
        """
        filename = file_path.name
        
        # Check hidden files
        if filename.startswith('.') and not self.get("include_hidden_files", False):
            return False
        
        # Check __pycache__ directories and .pyc files
        if not self.get("include_pycache", False):
            if filename == "__pycache__" or filename.endswith(('.pyc', '.pyo')):
                return False
            
            # Check if it's inside a __pycache__ directory
            if "__pycache__" in str(file_path):
                return False
        
        return True
    
    def should_include_file_contents(self, file_path: Path) -> bool:
        """
        Determine if a file's contents should be included based on configuration
        
        Args:
            file_path (Path): Path to the file to check
            
        Returns:
            bool: True if file contents should be included
        """
        extensions = self.get("include_file_contents", [])
        if not extensions:
            return False
        
        file_extension = file_path.suffix.lower()
        return file_extension in extensions
    
    def print_config(self) -> None:
        """Print current configuration"""
        print("Current Configuration:")
        print("=" * 40)
        for key, value in self.config.items():
            print(f"  {key}: {value}")
        print("=" * 40)
