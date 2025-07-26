import os
import argparse
from pathlib import Path

def print_tree_structure(folder_path, prefix="", output_file=None):
    """
    Print the directory structure in a tree format
    
    Args:
        folder_path (str or Path): Path to the folder to analyze
        prefix (str): Prefix for tree formatting
        output_file (file object): Optional file to write output to
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Error: The path '{folder_path}' does not exist.")
        return
    
    if not folder_path.is_dir():
        print(f"Error: The path '{folder_path}' is not a directory.")
        return
    
    def _print_directory_contents(dir_path, current_prefix=""):
        """Internal function to print directory contents without printing the directory name"""
        # Get all items in the directory, excluding hidden files/folders (starting with .)
        try:
            items = sorted([item for item in dir_path.iterdir() if not item.name.startswith('.')], 
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

def analyze_folder(target_folder, output_folder=None):
    """
    Analyze the target folder and optionally save results to output folder
    
    Args:
        target_folder (str): Path to the target folder to analyze
        output_folder (str, optional): Path to output folder where results will be saved
        
    Returns:
        str: Path to the output file if output_folder is specified, None otherwise
    """
    target_path = Path(target_folder)
    
    print(f"Analyzing folder structure of: {target_path.absolute()}")
    print("=" * 50)
    
    output_file = None
    output_file_path = None
    
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        output_file_path = output_path / "folder_structure.txt"
        output_file = open(output_file_path, 'w', encoding='utf-8')
        print(f"Results will be saved to: {output_file_path.absolute()}")
        print("=" * 50)
    
    try:
        print_tree_structure(target_path, output_file=output_file)
    finally:
        if output_file:
            output_file.close()
            print("=" * 50)
            print(f"Analysis complete! Results saved to: {output_file_path.absolute()}")
    
    return str(output_file_path) if output_file_path else None

def get_folder_structure_as_string(target_folder):
    """
    Get the folder structure as a string without printing to console
    
    Args:
        target_folder (str): Path to the target folder to analyze
        
    Returns:
        str: The folder structure as a formatted string
    """
    from io import StringIO
    
    # Capture output in a string buffer
    output_buffer = StringIO()
    
    def _capture_directory_contents(dir_path, current_prefix=""):
        """Internal function to capture directory contents without printing the directory name"""
        # Get all items in the directory, excluding hidden files/folders (starting with .)
        try:
            items = sorted([item for item in dir_path.iterdir() if not item.name.startswith('.')], 
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
    parser.add_argument("target_folder", help="Path to the target folder to analyze")
    parser.add_argument("-o", "--output", dest="output_folder", 
                       help="Path to output folder where results will be saved (optional)")
    return parser
