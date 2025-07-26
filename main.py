#!/usr/bin/env python3
"""
Folder Analysis Tool - Main Entry Point

This is the main entry point for the folder analysis tool.
The actual functionality is implemented in the src package.
"""

from src.folder_analyzer import analyze_folder, create_argument_parser
from src.config_manager import ConfigManager

def main():
    """Main function that handles command line arguments and calls the analyzer"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Load configuration
    config_manager = ConfigManager(args.config_file)
    
    # Show config and exit if requested
    if args.show_config:
        config_manager.print_config()
        return
    
    # Apply command line overrides
    if args.include_hidden:
        config_manager.set("include_hidden_files", True)
    
    if args.include_pycache:
        config_manager.set("include_pycache", True)
    
    if args.no_console:
        config_manager.set("output_to_console", False)
        config_manager.set("output_to_file", True)
    
    if args.include_contents is not None:
        config_manager.set("include_file_contents", args.include_contents)
    
    # Update config with command line arguments
    config_manager.update_from_args(args.target_folder, args.output_folder)
    
    # Validate that we have an input directory
    input_dir = config_manager.get("input_directory")
    if not input_dir:
        print("Error: No input directory specified. Provide it via command line or config file.")
        return
    
    # Run the analysis
    analyze_folder(config_manager=config_manager)

if __name__ == "__main__":
    main()
