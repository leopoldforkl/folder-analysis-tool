import os
import argparse
from pathlib import Path
from .config_manager import ConfigManager

def print_tree_structure(folder_path, prefix="", output_file=None, config_manager=None):
    """
    Print the directory structure in a tree format
    
    Args:
        folder_path (str or Path): Path to the folder to analyze
        prefix (str): Prefix for tree formatting
        output_file (file object): Optional file to write output to
        config_manager (ConfigManager, optional): Configuration manager instance
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Error: The path '{folder_path}' does not exist.")
        return
    
    if not folder_path.is_dir():
        print(f"Error: The path '{folder_path}' is not a directory.")
        return
    
    # Use default config if none provided
    if config_manager is None:
        config_manager = ConfigManager()
    
    def _print_directory_contents(dir_path, current_prefix=""):
        """Internal function to print directory contents without printing the directory name"""
        # Get all items in the directory, applying config-based filtering
        try:
            items = sorted([item for item in dir_path.iterdir() if config_manager.should_include_file(item)], 
                          key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            error_line = f"{current_prefix}├── [Permission Denied]"
            print(error_line)
            if output_file:
                output_file.write(error_line + "\n")
            return
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            
            if item.is_dir():
                # Directory
                current_prefix_symbol = "└── " if is_last else "├── "
                dir_line = f"{current_prefix}{current_prefix_symbol}{item.name}/"
                print(dir_line)
                if output_file:
                    output_file.write(dir_line + "\n")
                
                # Recursively print subdirectory contents
                next_prefix = current_prefix + ("    " if is_last else "│   ")
                _print_directory_contents(item, next_prefix)
            else:
                # File
                current_prefix_symbol = "└── " if is_last else "├── "
                file_line = f"{current_prefix}{current_prefix_symbol}{item.name}"
                print(file_line)
                if output_file:
                    output_file.write(file_line + "\n")
    
    # Print the root folder name only at the beginning
    root_line = f"{prefix}{folder_path.name}/"
    print(root_line)
    if output_file:
        output_file.write(root_line + "\n")
    
    # Print the contents
    _print_directory_contents(folder_path, prefix)

def collect_file_contents(folder_path, config_manager):
    """
    Collect contents of files matching configured extensions
    
    Args:
        folder_path (Path): Root folder to search
        config_manager (ConfigManager): Configuration manager instance
        
    Returns:
        List[Tuple[str, str]]: List of (relative_path, content) tuples
    """
    folder_path = Path(folder_path)
    file_contents = []
    
    try:
        for file_path in folder_path.rglob("*"):
            if file_path.is_file() and config_manager.should_include_file(file_path) and config_manager.should_include_file_contents(file_path):
                try:
                    # Try to read the file as text
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Get relative path from the root folder
                    relative_path = file_path.relative_to(folder_path)
                    file_contents.append((str(relative_path), content))
                    
                except (UnicodeDecodeError, PermissionError) as e:
                    # Skip binary files or files we can't read
                    relative_path = file_path.relative_to(folder_path)
                    file_contents.append((str(relative_path), f"[Could not read file: {e}]"))
                except Exception as e:
                    # Skip any other problematic files
                    relative_path = file_path.relative_to(folder_path)
                    file_contents.append((str(relative_path), f"[Error reading file: {e}]"))
    
    except Exception as e:
        print(f"Warning: Error collecting file contents: {e}")
    
    return file_contents

def analyze_folder(target_folder=None, output_folder=None, config_manager=None):
    """
    Analyze the target folder and optionally save results to output folder
    
    Args:
        target_folder (str, optional): Path to the target folder to analyze
        output_folder (str, optional): Path to output folder where results will be saved
        config_manager (ConfigManager, optional): Configuration manager instance
        
    Returns:
        str: Path to the output file if output_folder is specified, None otherwise
    """
    # Use default config if none provided
    if config_manager is None:
        config_manager = ConfigManager()
    
    # Use config values if parameters not provided
    if target_folder is None:
        target_folder = config_manager.get("input_directory", ".")
    
    if output_folder is None and config_manager.get("output_to_file", False):
        output_folder = config_manager.get("output_directory", "./output")
    
    target_path = Path(target_folder)
    
    if config_manager.get("output_to_console", True):
        print(f"Analyzing folder structure of: {target_path.absolute()}")
        print("=" * 50)
    
    output_file = None
    output_file_path = None
    
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        filename = config_manager.get("output_filename", "folder_structure.txt")
        output_file_path = output_path / filename
        output_file = open(output_file_path, 'w', encoding='utf-8')
        if config_manager.get("output_to_console", True):
            print(f"Results will be saved to: {output_file_path.absolute()}")
            print("=" * 50)
    
    try:
        if config_manager.get("output_to_console", True):
            print_tree_structure(target_path, output_file=output_file, config_manager=config_manager)
        elif output_file:
            # Only write to file, suppress console output
            print_tree_structure(target_path, output_file=output_file, config_manager=config_manager)
        
        # Add file contents to output file if configured
        if output_file and config_manager.get("include_file_contents", []):
            file_contents = collect_file_contents(target_path, config_manager)
            
            if file_contents:
                output_file.write("\n" + "=" * 60 + "\n")
                output_file.write("FILE CONTENTS\n")
                output_file.write("=" * 60 + "\n\n")
                
                for relative_path, content in file_contents:
                    output_file.write(f"{relative_path} contents:\n")
                    output_file.write("-" * 40 + "\n")
                    output_file.write(content)
                    if not content.endswith('\n'):
                        output_file.write('\n')
                    output_file.write("-" * 40 + "\n\n")
    finally:
        if output_file:
            output_file.close()
            if config_manager.get("output_to_console", True):
                print("=" * 50)
                print(f"Analysis complete! Results saved to: {output_file_path.absolute()}")
    
    return str(output_file_path) if output_file_path else None

def get_folder_structure_as_string(target_folder, config_manager=None):
    """
    Get the folder structure as a string without printing to console
    
    Args:
        target_folder (str): Path to the target folder to analyze
        config_manager (ConfigManager, optional): Configuration manager instance
        
    Returns:
        str: The folder structure as a formatted string
    """
    # Use default config if none provided
    if config_manager is None:
        config_manager = ConfigManager()
    from io import StringIO
    
    # Capture output in a string buffer
    output_buffer = StringIO()
    
    def _capture_directory_contents(dir_path, current_prefix=""):
        """Internal function to capture directory contents without printing the directory name"""
        # Get all items in the directory, applying config-based filtering
        try:
            items = sorted([item for item in dir_path.iterdir() if config_manager.should_include_file(item)], 
                          key=lambda x: (x.is_file(), x.name.lower()))
        except PermissionError:
            output_buffer.write(f"{current_prefix}├── [Permission Denied]\n")
            return
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            
            if item.is_dir():
                # Directory
                current_prefix_symbol = "└── " if is_last else "├── "
                output_buffer.write(f"{current_prefix}{current_prefix_symbol}{item.name}/\n")
                
                # Recursively process subdirectory contents
                next_prefix = current_prefix + ("    " if is_last else "│   ")
                _capture_directory_contents(item, next_prefix)
            else:
                # File
                current_prefix_symbol = "└── " if is_last else "├── "
                output_buffer.write(f"{current_prefix}{current_prefix_symbol}{item.name}\n")
    
    folder_path = Path(target_folder)
    
    if not folder_path.exists():
        output_buffer.write(f"Error: The path '{folder_path}' does not exist.\n")
        result = output_buffer.getvalue()
        output_buffer.close()
        return result
    
    if not folder_path.is_dir():
        output_buffer.write(f"Error: The path '{folder_path}' is not a directory.\n")
        result = output_buffer.getvalue()
        output_buffer.close()
        return result
    
    # Write the root folder name
    output_buffer.write(f"{folder_path.name}/\n")
    
    # Capture the contents
    _capture_directory_contents(folder_path)
    
    result = output_buffer.getvalue()
    output_buffer.close()
    
    return result

def create_argument_parser():
    """
    Create and return the argument parser for command line usage
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(description="Analyze folder structure and print it in tree format")
    parser.add_argument("target_folder", nargs="?", help="Path to the target folder to analyze (optional if set in config)")
    parser.add_argument("-o", "--output", dest="output_folder", 
                       help="Path to output folder where results will be saved (optional)")
    parser.add_argument("-c", "--config", dest="config_file", default="config.json",
                       help="Path to configuration file (default: config.json)")
    parser.add_argument("--show-config", action="store_true",
                       help="Show current configuration and exit")
    parser.add_argument("--include-hidden", action="store_true",
                       help="Include hidden files and folders (overrides config)")
    parser.add_argument("--include-pycache", action="store_true",
                       help="Include __pycache__ files and folders (overrides config)")
    parser.add_argument("--no-console", action="store_true",
                       help="Suppress console output (only save to file)")
    parser.add_argument("--include-contents", nargs="*", metavar="EXT",
                       help="Include file contents for specified extensions (e.g., --include-contents .py .json)")
    return parser
