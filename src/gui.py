import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
from typing import Set, Dict, List, Tuple
from .config_manager import ConfigManager
from .folder_analyzer import analyze_folder, collect_file_contents


class FolderAnalysisGUI:
    """GUI application for the folder analysis tool"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Folder Analysis Tool")
        self.root.geometry("800x600")
        
        # Application state
        self.config_manager = ConfigManager()
        self.output_folder = None
        self.target_folder = None
        self.selected_items = set()  # Set of Path objects
        self.content_extensions = set()  # Set of file extensions to include contents for
        
        # Current step
        self.current_step = 0
        self.steps = [
            "Select Output Folder",
            "Select Target Folder and Files",
            "Choose Content Extraction"
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the main UI structure"""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Header
        self.setup_header()
        
        # Content area (will change based on step)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Navigation buttons
        self.setup_navigation()
        
        # Show first step
        self.show_step()
        
    def setup_header(self):
        """Set up the header with step information"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Step indicator
        self.step_label = ttk.Label(header_frame, text="", font=("Arial", 14, "bold"))
        self.step_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        # Progress bar
        self.progress = ttk.Progressbar(header_frame, length=400, mode='determinate')
        self.progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
    def setup_navigation(self):
        """Set up navigation buttons"""
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Back button
        self.back_btn = ttk.Button(nav_frame, text="Back", command=self.go_back)
        self.back_btn.pack(side=tk.LEFT)
        
        # Next/Finish button
        self.next_btn = ttk.Button(nav_frame, text="Next", command=self.go_next)
        self.next_btn.pack(side=tk.RIGHT)
        
        # Cancel button
        cancel_btn = ttk.Button(nav_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
    def update_header(self):
        """Update header information"""
        step_text = f"Step {self.current_step + 1} of {len(self.steps)}: {self.steps[self.current_step]}"
        self.step_label.config(text=step_text)
        self.progress['value'] = ((self.current_step + 1) / len(self.steps)) * 100
        
        # Update navigation buttons
        self.back_btn.config(state='normal' if self.current_step > 0 else 'disabled')
        if self.current_step == len(self.steps) - 1:
            self.next_btn.config(text="Analyze")
        else:
            self.next_btn.config(text="Next")
            
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_step(self):
        """Show the current step"""
        self.clear_content()
        self.update_header()
        
        if self.current_step == 0:
            self.show_output_selection()
        elif self.current_step == 1:
            self.show_file_selection()
        elif self.current_step == 2:
            self.show_content_selection()
            
    def show_output_selection(self):
        """Step 1: Select output folder"""
        # Title
        title = ttk.Label(self.content_frame, text="Select Output Folder", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Description
        desc = ttk.Label(self.content_frame, 
                        text="Choose where to save the analysis results.",
                        wraplength=400)
        desc.grid(row=1, column=0, pady=(0, 20))
        
        # Current selection
        selection_frame = ttk.LabelFrame(self.content_frame, text="Selected Output Folder", padding="10")
        selection_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        selection_frame.columnconfigure(0, weight=1)
        
        self.output_label = ttk.Label(selection_frame, text=self.output_folder or "No folder selected")
        self.output_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Browse button
        browse_btn = ttk.Button(selection_frame, text="Browse...", command=self.browse_output_folder)
        browse_btn.grid(row=1, column=0, pady=(10, 0))
        
    def show_file_selection(self):
        """Step 2: Select target folder and files"""
        # Title
        title = ttk.Label(self.content_frame, text="Select Files and Folders", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Description
        desc = ttk.Label(self.content_frame, 
                        text="Choose a target folder to analyze. You can optionally select specific files/folders, or leave nothing selected to analyze the entire folder.",
                        wraplength=500)
        desc.grid(row=1, column=0, columnspan=2, pady=(0, 15))
        
        # Target folder selection
        folder_frame = ttk.LabelFrame(self.content_frame, text="Target Folder", padding="5")
        folder_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(0, weight=1)
        
        self.target_label = ttk.Label(folder_frame, text=self.target_folder or "No folder selected")
        self.target_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        browse_target_btn = ttk.Button(folder_frame, text="Browse...", command=self.browse_target_folder)
        browse_target_btn.grid(row=1, column=0, pady=(5, 0))
        
        if self.target_folder:
            # File tree
            tree_frame = ttk.LabelFrame(self.content_frame, text="Select Files and Folders", padding="5")
            tree_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
            tree_frame.columnconfigure(0, weight=1)
            tree_frame.rowconfigure(0, weight=1)
            
            # Create treeview with checkboxes
            self.tree = ttk.Treeview(tree_frame, columns=('selected', 'path'), height=15)
            self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Configure columns
            self.tree.heading('#0', text='Name')
            self.tree.heading('selected', text='Selected')
            self.tree.column('selected', width=80)
            # Hide the path column (used for internal storage only)
            self.tree.column('path', width=0, stretch=False)
            self.tree.heading('path', text='')  # No heading for hidden column
            
            # Scrollbars
            v_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
            v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
            self.tree.configure(yscrollcommand=v_scroll.set)
            
            h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
            h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
            self.tree.configure(xscrollcommand=h_scroll.set)
            
            # Bind events
            self.tree.bind('<Double-1>', self.toggle_selection)
            self.tree.bind('<space>', self.toggle_selection)
            
            # Populate tree
            self.populate_tree()
            
            # Selection info
            info_frame = ttk.Frame(self.content_frame)
            info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
            
            ttk.Label(info_frame, text="Double-click or press Space to select/deselect items").pack(side=tk.LEFT)
            
            self.selection_count_label = ttk.Label(info_frame, text=f"Selected: {len(self.selected_items)} items")
            self.selection_count_label.pack(side=tk.RIGHT)
            
    def show_content_selection(self):
        """Step 3: Choose content extraction options"""
        # Title
        title = ttk.Label(self.content_frame, text="Content Extraction Options", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, pady=(0, 20))
        
        # Description
        desc = ttk.Label(self.content_frame, 
                        text="Select file types for which you want to include the actual file contents in the output.",
                        wraplength=500)
        desc.grid(row=1, column=0, pady=(0, 20))
        
        # Get unique extensions from selected files
        extensions = self.get_selected_extensions()
        
        if extensions:
            # Extension selection
            ext_frame = ttk.LabelFrame(self.content_frame, text="File Extensions", padding="10")
            ext_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
            
            self.extension_vars = {}
            row = 0
            col = 0
            
            for ext in sorted(extensions):
                var = tk.BooleanVar()
                # Check if extension was previously selected or is in config
                if ext in self.content_extensions or ext in self.config_manager.get("include_file_contents", []):
                    var.set(True)
                    self.content_extensions.add(ext)
                
                cb = ttk.Checkbutton(ext_frame, text=ext, variable=var,
                                   command=lambda e=ext, v=var: self.toggle_extension(e, v))
                cb.grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
                
                self.extension_vars[ext] = var
                
                col += 1
                if col > 3:  # 4 columns
                    col = 0
                    row += 1
                    
            # Select all / None buttons
            btn_frame = ttk.Frame(ext_frame)
            btn_frame.grid(row=row+1, column=0, columnspan=4, pady=(10, 0))
            
            ttk.Button(btn_frame, text="Select All", command=self.select_all_extensions).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Select None", command=self.select_no_extensions).pack(side=tk.LEFT, padx=5)
            
        else:
            # No files selected
            no_files_label = ttk.Label(self.content_frame, text="No files selected for analysis.")
            no_files_label.grid(row=2, column=0, pady=20)
            
        # Summary
        summary_frame = ttk.LabelFrame(self.content_frame, text="Analysis Summary", padding="10")
        summary_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        summary_text = f"• Selected items: {len(self.selected_items)}\n"
        summary_text += f"• Content extraction: {len(self.content_extensions)} file types\n"
        summary_text += f"• Output folder: {self.output_folder}"
        
        ttk.Label(summary_frame, text=summary_text, justify=tk.LEFT).pack(anchor=tk.W)
        
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder",
                                       initialdir=self.config_manager.get("output_directory", "."))
        if folder:
            self.output_folder = folder
            self.output_label.config(text=folder)
            
    def browse_target_folder(self):
        """Browse for target folder"""
        folder = filedialog.askdirectory(title="Select Target Folder",
                                       initialdir=self.config_manager.get("input_directory", "."))
        if folder:
            self.target_folder = folder
            self.target_label.config(text=folder)
            self.selected_items.clear()  # Clear previous selections
            self.show_step()  # Refresh to show file tree
            
    def populate_tree(self):
        """Populate the file tree"""
        if not self.target_folder:
            return
            
        self.tree.delete(*self.tree.get_children())
        
        target_path = Path(self.target_folder)
        
        # Add root item
        root_item = self.tree.insert('', 'end', text=target_path.name, values=('☐',))
        self.tree.set(root_item, 'path', str(target_path))
        
        # Recursively add items
        self.add_tree_items(root_item, target_path)
        
        # Expand root
        self.tree.item(root_item, open=True)
        
    def add_tree_items(self, parent_item, path, max_depth=3, current_depth=0):
        """Recursively add items to tree"""
        if current_depth >= max_depth:
            return
            
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            
            for item in items:
                if self.config_manager.should_include_file(item):
                    is_selected = item in self.selected_items
                    checkbox = '☑' if is_selected else '☐'
                    
                    tree_item = self.tree.insert(parent_item, 'end', 
                                                text=item.name + ('/' if item.is_dir() else ''),
                                                values=(checkbox,))
                    self.tree.set(tree_item, 'path', str(item))
                    
                    if item.is_dir() and current_depth < max_depth - 1:
                        self.add_tree_items(tree_item, item, max_depth, current_depth + 1)
                        
        except PermissionError:
            # Add permission denied item
            self.tree.insert(parent_item, 'end', text="[Permission Denied]", values=('',))
            
    def toggle_selection(self, event=None):
        """Toggle selection of tree item"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return
            
        path_str = self.tree.set(item, 'path')
        if not path_str:
            return
            
        path = Path(path_str)
        
        if path in self.selected_items:
            self.selected_items.remove(path)
            # Also remove any children
            self.remove_children_from_selection(path)
            checkbox = '☐'
        else:
            self.selected_items.add(path)
            # If it's a directory, add all its contents
            if path.is_dir():
                self.add_children_to_selection(path)
            checkbox = '☑'
            
        self.tree.set(item, 'selected', checkbox)
        self.update_tree_checkboxes()
        
        if hasattr(self, 'selection_count_label'):
            self.selection_count_label.config(text=f"Selected: {len(self.selected_items)} items")
            
    def add_children_to_selection(self, dir_path):
        """Add all children of a directory to selection"""
        try:
            for item in dir_path.rglob("*"):
                if self.config_manager.should_include_file(item):
                    self.selected_items.add(item)
        except PermissionError:
            pass
            
    def remove_children_from_selection(self, dir_path):
        """Remove all children of a directory from selection"""
        to_remove = [item for item in self.selected_items if str(item).startswith(str(dir_path) + os.sep)]
        for item in to_remove:
            self.selected_items.discard(item)
            
    def update_tree_checkboxes(self):
        """Update all checkboxes in the tree"""
        def update_item(item):
            path_str = self.tree.set(item, 'path')
            if path_str:
                path = Path(path_str)
                checkbox = '☑' if path in self.selected_items else '☐'
                self.tree.set(item, 'selected', checkbox)
                
            for child in self.tree.get_children(item):
                update_item(child)
                
        for root_item in self.tree.get_children():
            update_item(root_item)
            
    def get_selected_extensions(self):
        """Get unique file extensions from selected files"""
        extensions = set()
        for item in self.selected_items:
            if item.is_file():
                ext = item.suffix.lower()
                if ext:
                    extensions.add(ext)
        return extensions
        
    def toggle_extension(self, ext, var):
        """Toggle extension selection"""
        if var.get():
            self.content_extensions.add(ext)
        else:
            self.content_extensions.discard(ext)
            
    def select_all_extensions(self):
        """Select all extensions"""
        for ext, var in self.extension_vars.items():
            var.set(True)
            self.content_extensions.add(ext)
            
    def select_no_extensions(self):
        """Deselect all extensions"""
        for ext, var in self.extension_vars.items():
            var.set(False)
            self.content_extensions.discard(ext)
            
    def go_back(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()
            
    def go_next(self):
        """Go to next step or finish"""
        if self.current_step == len(self.steps) - 1:
            self.finish_analysis()
        else:
            if self.validate_current_step():
                self.current_step += 1
                self.show_step()
                
    def validate_current_step(self):
        """Validate current step before proceeding"""
        if self.current_step == 0:
            if not self.output_folder:
                messagebox.showerror("Error", "Please select an output folder.")
                return False
        elif self.current_step == 1:
            if not self.target_folder:
                messagebox.showerror("Error", "Please select a target folder.")
                return False
            # Allow proceeding with no selections (analyze entire folder) or with selections
            # No validation needed for selected_items - empty means analyze everything
        return True
        
    def finish_analysis(self):
        """Perform the analysis"""
        try:
            # Update config with selections
            self.config_manager.set("include_file_contents", list(self.content_extensions))
            
            if self.selected_items:
                # If specific items are selected, create a temporary directory structure
                import tempfile
                import shutil
                
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    target_path = Path(self.target_folder)
                    
                    # Create a subdirectory with the target folder's name
                    target_folder_name = target_path.name
                    analysis_root = temp_path / target_folder_name
                    analysis_root.mkdir(exist_ok=True)
                    
                    # Copy selected items to temporary structure
                    for item in self.selected_items:
                        if item.exists():
                            rel_path = item.relative_to(target_path)
                            dest_path = analysis_root / rel_path
                            
                            if item.is_file():
                                dest_path.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(item, dest_path)
                            elif item.is_dir():
                                # Copy entire directory
                                dest_path.mkdir(parents=True, exist_ok=True)
                                for sub_item in item.rglob("*"):
                                    if self.config_manager.should_include_file(sub_item):
                                        sub_rel_path = sub_item.relative_to(target_path)
                                        sub_dest_path = analysis_root / sub_rel_path
                                        
                                        if sub_item.is_file():
                                            sub_dest_path.parent.mkdir(parents=True, exist_ok=True)
                                            try:
                                                shutil.copy2(sub_item, sub_dest_path)
                                            except (PermissionError, OSError):
                                                pass  # Skip files we can't copy
                    
                    # Perform analysis on temporary structure
                    output_file = analyze_folder(
                        target_folder=str(analysis_root),
                        output_folder=self.output_folder,
                        config_manager=self.config_manager
                    )
            else:
                # If no specific items selected, analyze the entire target folder
                output_file = analyze_folder(
                    target_folder=self.target_folder,
                    output_folder=self.output_folder,
                    config_manager=self.config_manager
                )
                
            messagebox.showinfo("Success", 
                              f"Analysis completed successfully!\n\nResults saved to:\n{output_file}")
            self.root.quit()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis:\n{str(e)}")
            
    def cancel(self):
        """Cancel the wizard"""
        if messagebox.askokcancel("Cancel", "Are you sure you want to cancel?"):
            self.root.quit()
            
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()


def run_gui():
    """Run the GUI application"""
    app = FolderAnalysisGUI()
    app.run()
