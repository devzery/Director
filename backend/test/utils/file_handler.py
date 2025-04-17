import json
import os
from typing import Dict, Any, Union, List

class FileHandler:
    """Utility class to handle JSON file operations."""

    @staticmethod
    def load_json(file_path: str) -> Union[Dict[str, Any], List[Any]]:
        """
        Load and parse a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            Union[Dict[str, Any], List[Any]]: Parsed JSON content.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at {file_path} does not exist.")
            
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    @staticmethod
    def save_json(file_path: str, data: Union[Dict[str, Any], List[Any]], indent: int = 4) -> None:
        """
        Save data to a JSON file.

        Args:
            file_path (str): Path where to save the JSON file.
            data (Union[Dict[str, Any], List[Any]]): Data to save.
            indent (int, optional): Indentation level for the JSON file. Defaults to 4.
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent)