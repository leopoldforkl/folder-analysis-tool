import os
import fnmatch

# run with python map_repo.py

OUTPUT_FILE = "repo_structure.txt"

def parse_gitignore(root_dir):
    """Reads .gitignore and returns a list of patterns to ignore."""
    patterns = ['.git', OUTPUT_FILE] 
    gitignore_path = os.path.join(root_dir, '.gitignore')
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('!'):
                    continue
                patterns.append(line)
    return patterns

def is_ignored(rel_path, patterns):
    """Checks if a given relative path matches any gitignore pattern."""
    rel_path = rel_path.replace(os.sep, '/')
    for pattern in patterns:
        if pattern.endswith('/'):
            pattern = pattern[:-1]
        if fnmatch.fnmatch(rel_path, pattern):
            return True
        basename = rel_path.split('/')[-1]
        if fnmatch.fnmatch(basename, pattern):
            return True
        if pattern in rel_path.split('/'):
            return True
        if pattern.startswith('/'):
            if fnmatch.fnmatch(rel_path, pattern[1:]) or rel_path.startswith(pattern[1:] + '/'):
                return True
    return False

def is_text_file(filepath):
    """Heuristic to determine if a file is text (readable) or binary."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
        # If it contains null bytes, it's almost certainly binary
        if b'\x00' in chunk:
            return False
        # Try decoding it to catch other non-utf-8 binary formats
        chunk.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False
    except Exception:
        return False # Fallback for permission errors, etc.

def build_tree(root_dir, patterns, file_obj, included_files, prefix=""):
    """Recursively walks the directory, prints tree, and collects file paths."""
    try:
        items = os.listdir(root_dir)
    except PermissionError:
        return

    folders = []
    files = []
    
    for item in items:
        full_path = os.path.join(root_dir, item)
        rel_path = os.path.relpath(full_path, start=os.getcwd())
        
        if is_ignored(rel_path, patterns):
            continue
            
        if os.path.isdir(full_path):
            folders.append(item)
        else:
            files.append(item)
            
    folders.sort(key=lambda s: s.lower())
    files.sort(key=lambda s: s.lower())
    
    all_items = folders + files
    count = len(all_items)
    
    for i, item in enumerate(all_items):
        full_path = os.path.join(root_dir, item)
        is_last = (i == count - 1)
        
        connector = "└── " if is_last else "├── "
        file_obj.write(f"{prefix}{connector}{item}\n")
        
        if os.path.isdir(full_path):
            extension = "    " if is_last else "│   "
            build_tree(full_path, patterns, file_obj, included_files, prefix + extension)
        else:
            included_files.append(full_path)

if __name__ == "__main__":
    cwd = os.getcwd()
    print(f"Analyzing repository at: {cwd}")
    
    ignore_patterns = parse_gitignore(cwd)
    print(f"Loaded {len(ignore_patterns) - 2} patterns from .gitignore")
    
    output_path = os.path.join(cwd, OUTPUT_FILE)
    included_files = []
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # 1. Write the tree structure
        root_name = os.path.basename(cwd)
        f.write(f"{root_name}/\n")
        build_tree(cwd, ignore_patterns, f, included_files)
        
        # 2. Write the file contents
        f.write("\n\n" + "="*60 + "\n")
        f.write("File-Contents:\n")
        f.write("="*60 + "\n\n")
        
        appended_count = 0
        for filepath in included_files:
            rel_path = os.path.relpath(filepath, start=cwd)
            
            if is_text_file(filepath):
                f.write(f"\n--- {rel_path} ---\n")
                try:
                    with open(filepath, 'r', encoding='utf-8') as src:
                        f.write(src.read())
                        if not f.tell() == 0: # Ensure file doesn't end without a newline
                            f.write("\n")
                except Exception as e:
                    f.write(f"[Error reading file: {e}]\n")
                f.write(f"--- EOF: {rel_path} ---\n\n")
                appended_count += 1
            else:
                f.write(f"\n--- {rel_path} ---\n")
                f.write("[Binary or unreadable file skipped]\n")
                f.write(f"--- EOF: {rel_path} ---\n\n")
                
    print(f"Done! Tree structure and {appended_count} text files saved to: {OUTPUT_FILE}")