# Folder Analysis Tool

A Python tool that analyzes folder structures and generates tree-like visualizations of directory contents. The tool can print the structure to console or save it to a text file for documentation purposes.

## Features

- 🌳 **Tree Visualization**: Displays folder structures in a clean, tree-like format
- ⚙️ **Configuration File**: JSON-based configuration for default settings
- 📁 **Hidden File Filtering**: Configurable inclusion/exclusion of hidden files and folders (starting with `.`)
- � **Python Cache Control**: Configurable inclusion/exclusion of `__pycache__` directories and `.pyc` files
- �💾 **Output to File**: Optionally saves analysis results to a text file
- 🔧 **Programmatic API**: Can be used as a Python module for integration into other projects
- 📊 **Statistical Analysis**: Provides summary statistics about directory contents
- 🧪 **Interactive Testing**: Includes Jupyter notebook for testing and experimentation
- 🎛️ **Command Line Overrides**: Override configuration settings from command line

## Installation

Clone the repository:
```bash
git clone https://github.com/leopoldforkl/folder-analysis-tool.git
cd folder-analysis-tool
```

No additional dependencies required - uses only Python standard library.

## Usage

### Configuration File

The tool uses a `config.json` file for default settings. If it doesn't exist, it will be created automatically:

```json
{
    "input_directory": ".",
    "output_directory": "./output",
    "include_hidden_files": false,
    "include_pycache": false,
    "output_to_console": true,
    "output_to_file": true,
    "output_filename": "folder_structure.txt"
}
```

**Configuration Options:**
- `input_directory`: Default directory to analyze
- `output_directory`: Default output directory for results
- `include_hidden_files`: Include files/folders starting with `.`
- `include_pycache`: Include `__pycache__` directories and `.pyc` files
- `output_to_console`: Print results to console
- `output_to_file`: Save results to file
- `output_filename`: Name of the output file

### Command Line Interface

**Show current configuration:**
```bash
python main.py --show-config
```

**Basic usage (uses config settings):**
```bash
python main.py
```

**Specify target folder:**
```bash
python main.py "C:\path\to\target\folder"
```

**With output folder:**
```bash
python main.py "C:\path\to\target\folder" -o "C:\path\to\output\folder"
```

**Include hidden files:**
```bash
python main.py --include-hidden
```

**Include Python cache files:**
```bash
python main.py --include-pycache
```

**Suppress console output (file only):**
```bash
python main.py --no-console -o "./output"
```

**Use custom config file:**
```bash
python main.py -c "my_config.json"
```

### Programmatic Usage

```python
from src.folder_analyzer import analyze_folder, get_folder_structure_as_string
from src.config_manager import ConfigManager

# Use with custom configuration
config = ConfigManager("my_config.json")
config.set("include_hidden_files", True)
config.set("include_pycache", False)

# Get structure as string
structure = get_folder_structure_as_string("C:/some/folder", config)
print(structure)

# Analyze with configuration
output_file = analyze_folder(config_manager=config)

# Or use defaults
structure = get_folder_structure_as_string("C:/some/folder")
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
├── config.json                      # Configuration file
├── src/
│   ├── __init__.py                  # Package initialization
│   ├── folder_analyzer.py           # Core functionality
│   └── config_manager.py            # Configuration management
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
- **`ConfigManager`** - Manages configuration settings and file filtering rules

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
