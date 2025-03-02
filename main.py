import os
import ctypes
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", f'"{__file__}"', None, 1)
    exit()

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

class HostsManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hosts File Manager")
        self.geometry("800x600")
        self.configure(bg='#f0f0f0')
        self.hosts_entries = []
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=25)
        self.style.configure('Custom.TButton', padding=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        
        # Default IP for all entries
        self.default_ip = "127.0.0.1"
        
        self.load_hosts_file()
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def load_hosts_file(self):
        try:
            self.hosts_entries = []
            with open(HOSTS_PATH, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) > 1:
                            # Check if this is a comment line with domains
                            comment = ""
                            domains = []
                            
                            if parts[0] == self.default_ip:
                                # Extract domains and possible comment
                                for part in parts[1:]:
                                    if part.startswith('#'):
                                        # Everything after # is a comment
                                        comment_index = line.find('#')
                                        if comment_index > -1:
                                            comment = line[comment_index:].strip()
                                        break
                                    domains.append(part)
                                
                                self.hosts_entries.append({'domains': domains, 'comment': comment})
            self.show_status("Hosts file loaded successfully", 'success')
        except Exception as e:
            self.show_status(f"Error loading hosts file: {str(e)}", 'error')

    def save_hosts_file(self):
        try:
            # Read the current content of the hosts file
            with open(HOSTS_PATH, 'r') as f:
                current_lines = f.readlines()

            # Create a set of active entries for easy lookup
            active_entries = set()
            for entry in self.hosts_entries:
                domains_str = ' '.join(entry['domains'])
                active_entries.add(f"{self.default_ip} {domains_str}")

            # Process the file line by line
            new_lines = []
            for line in current_lines:
                line = line.rstrip('\n')
                # Preserve comments and empty lines
                if not line.strip() or line.strip().startswith('#'):
                    new_lines.append(line)
                    continue
                
                # Check if this line is an active entry
                parts = line.strip().split()
                if len(parts) > 1 and parts[0] == self.default_ip:
                    # Extract just the domains part for comparison
                    domains_part = ' '.join(parts[1:])
                    # Remove any comments from the domains part for comparison
                    if '#' in domains_part:
                        domains_part = domains_part[:domains_part.find('#')].strip()
                    
                    entry_to_check = f"{self.default_ip} {domains_part}"
                    if entry_to_check not in active_entries:
                        continue

            # Add any new entries that weren't in the original file
            for entry in self.hosts_entries:
                domains_str = ' '.join(entry['domains'])
                entry_str = f"{self.default_ip} {domains_str}"
                
                # Add comment if present
                if entry.get('comment', ''):
                    entry_str += f" {entry['comment']}"
                    
                if entry_str not in [line.strip() for line in new_lines if line.strip()]:
                    new_lines.append(entry_str)

            # Write back to the file, preserving newlines
            with open(HOSTS_PATH, 'w') as f:
                for line in new_lines:
                    f.write(f"{line}\n")

            subprocess.run(['ipconfig', '/flushdns'], shell=True, capture_output=True)
            self.show_status("Changes saved successfully", 'success')
            return True
        except Exception as e:
            self.show_status(f"Error saving changes: {str(e)}", 'error')
            return False

    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_container,
            text="Hosts File Manager",
            font=('Helvetica', 16, 'bold'),
            padding=(0, 0, 0, 10)
        )
        title_label.pack()

        # Treeview with scrollbar
        tree_frame = ttk.Frame(main_container)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.tree = ttk.Treeview(tree_frame, columns=('Domains', 'Comment'), show='headings')
        self.tree.heading('Domains', text='Domains')
        self.tree.heading('Comment', text='Comment')
        self.tree.column('Domains', width=500)
        self.tree.column('Comment', width=250)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Control buttons
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(pady=10)
        
        # Buttons with icons and tooltips
        buttons = [
            ("Add Entry", self.add_entry, "Add a new hosts entry"),
            ("Edit Entry", self.edit_entry, "Edit selected hosts entry"),
            ("Delete Entry", self.delete_entry, "Delete selected hosts entry"),
            ("Open File", self.open_hosts_file, "Open hosts file in text editor"),
            ("Refresh", self.refresh_list, "Reload hosts file"),
            ("Exit", self.destroy, "Close application")
        ]

        for i, (text, command, tooltip) in enumerate(buttons):
            btn = ttk.Button(btn_frame, text=text, command=command, style='Custom.TButton')
            btn.grid(row=0, column=i, padx=5)
            self.create_tooltip(btn, tooltip)

        # Status bar
        status_frame = ttk.Frame(main_container, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W, padx=5, pady=2)

        self.refresh_list()

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief=tk.SOLID, borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)

    def show_status(self, message, status_type='info'):
        colors = {
            'success': '#28a745',
            'error': '#dc3545',
            'info': '#17a2b8'
        }
        self.status_var.set(message)
        self.after(3000, lambda: self.status_var.set(''))

    def refresh_list(self):
        self.load_hosts_file()
        self.tree.delete(*self.tree.get_children())
        for entry in self.hosts_entries:
            comment = entry.get('comment', '')
            self.tree.insert('', 'end', values=(', '.join(entry['domains']), comment))
        self.show_status("List refreshed", 'info')

    def add_entry(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add New Entry")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Domains:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        domains_entry = ttk.Entry(frame, width=30)
        domains_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame, text="(space-separated)", font=('Helvetica', 8)).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Comment:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        comment_entry = ttk.Entry(frame, width=30)
        comment_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(frame, text="(optional)", font=('Helvetica', 8)).grid(row=1, column=2, padx=5, pady=5)
        
        def save():
            domains = domains_entry.get().strip().split()
            comment = comment_entry.get().strip()
            
            if comment and not comment.startswith('#'):
                comment = f"# {comment}"
                
            if domains:
                self.hosts_entries.append({'domains': domains, 'comment': comment})
                if self.save_hosts_file():
                    self.refresh_list()
                    dialog.destroy()
            else:
                messagebox.showerror("Error", "Domain(s) are required", parent=dialog)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=save, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy, style='Custom.TButton').pack(side=tk.LEFT, padx=5)

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an entry to edit")
            return
        
        index = self.tree.index(selected[0])
        entry = self.hosts_entries[index]
        
        dialog = tk.Toplevel(self)
        dialog.title("Edit Entry")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Domains:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        domains_entry = ttk.Entry(frame, width=30)
        domains_entry.grid(row=0, column=1, padx=5, pady=5)
        domains_entry.insert(0, ' '.join(entry['domains']))
        ttk.Label(frame, text="(space-separated)", font=('Helvetica', 8)).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Comment:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        comment_entry = ttk.Entry(frame, width=30)
        comment_entry.grid(row=1, column=1, padx=5, pady=5)
        comment_entry.insert(0, entry.get('comment', '').replace('# ', ''))
        
        def save():
            domains = domains_entry.get().strip().split()
            comment = comment_entry.get().strip()
            
            if comment and not comment.startswith('#'):
                comment = f"# {comment}"
                
            if domains:
                self.hosts_entries[index]['domains'] = domains
                self.hosts_entries[index]['comment'] = comment
                if self.save_hosts_file():
                    self.refresh_list()
                    dialog.destroy()
            else:
                messagebox.showerror("Error", "Domain(s) are required", parent=dialog)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="Save", command=save, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy, style='Custom.TButton').pack(side=tk.LEFT, padx=5)

    def open_hosts_file(self):
        try:
            subprocess.run(['notepad.exe', HOSTS_PATH], shell=True, check=True)
            self.show_status("Hosts file opened successfully", 'success')
        except Exception as e:
            self.show_status(f"Error opening hosts file: {str(e)}", 'error')

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
        
        entry = self.hosts_entries[self.tree.index(selected[0])]
        if messagebox.askyesno("Confirm Delete", 
                             f"Are you sure you want to delete the following entry?\n\n" 
                             f"Domains: {', '.join(entry['domains'])}\n" 
                             f"Comment: {entry.get('comment', '')}"):
            index = self.tree.index(selected[0])
            del self.hosts_entries[index]
            if self.save_hosts_file():
                self.refresh_list()
                self.show_status("Entry deleted successfully", 'success')

if __name__ == "__main__":
    app = HostsManager()
    app.mainloop()