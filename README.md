# Folder Analysis Tool

A Python tool that analyzes folder structures and generates tree-like visualizations of directory contents. The tool can print the structure to console or save it to a text file for documentation purposes.

## Features

- 🌳 **Tree Visualization**: Displays folder structures in a clean, tree-like format
- 📁 **Hidden File Filtering**: Automatically excludes hidden files and folders (starting with `.`)
- 💾 **Output to File**: Optionally saves analysis results to a text file
- 🔧 **Programmatic API**: Can be used as a Python module for integration into other projects
- 📊 **Statistical Analysis**: Provides summary statistics about directory contents
- 🧪 **Interactive Testing**: Includes Jupyter notebook for testing and experimentation

## Installation

Clone the repository:
```bash
git clone https://github.com/leopoldforkl/folder-analysis-tool.git
cd folder-analysis-tool
```

No additional dependencies required - uses only Python standard library.

## Usage

### Command Line Interface

**Basic usage (print to console):**
```bash
python main.py "C:\path\to\target\folder"
```

**With output file:**
```bash
python main.py "C:\path\to\target\folder" -o "C:\path\to\output\folder"
```

### Programmatic Usage

```python
from src.folder_analyzer import analyze_folder, get_folder_structure_as_string

# Get structure as string
structure = get_folder_structure_as_string("C:/some/folder")
print(structure)

# Analyze with output file
output_file = analyze_folder("C:/target", "C:/output")
```

## Example Output

```
my_project/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── docs/
│   └── README.md
└── requirements.txt
```

## Project Structure

```
folder-analysis-tool/
├── main.py                          # Command line entry point
├── src/
│   ├── __init__.py                  # Package initialization
│   └── folder_analyzer.py           # Core functionality
├── notebooks/
│   └── test_folder_analyzer.ipynb   # Interactive testing notebook
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## Core Functions

- **`print_tree_structure()`** - Prints folder structure in tree format
- **`analyze_folder()`** - Main analysis function with optional file output
- **`get_folder_structure_as_string()`** - Returns structure as string for programmatic use
- **`create_argument_parser()`** - Creates command line argument parser

## Testing

The project includes a comprehensive Jupyter notebook for testing:

```bash
# Open the testing notebook
jupyter notebook notebooks/test_folder_analyzer.ipynb
```

The notebook demonstrates:
- Creating test directory structures
- Testing all core functions
- Generating statistical analysis
- Validating output formats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test using the provided notebook
5. Submit a pull request

## License

This project is open source and available under the MIT License.
