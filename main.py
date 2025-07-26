#!/usr/bin/env python3
"""
Folder Analysis Tool - Main Entry Point

This is the main entry point for the folder analysis tool.
The actual functionality is implemented in the src package.
"""

from src.folder_analyzer import analyze_folder, create_argument_parser

def main():
    """Main function that handles command line arguments and calls the analyzer"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    analyze_folder(args.target_folder, args.output_folder)

if __name__ == "__main__":
    main()
