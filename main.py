import os
import ctypes
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

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
        self.geometry("800x500")
        self.hosts_entries = []
        self.load_hosts_file()
        self.create_widgets()
        
    def load_hosts_file(self):
        self.hosts_entries = []
        with open(HOSTS_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) > 1:
                        ip = parts[0]
                        domains = parts[1:]
                        self.hosts_entries.append({'ip': ip, 'domains': domains, 'raw': line})

    def save_hosts_file(self):
        with open(HOSTS_PATH, 'w') as f:
            for entry in self.hosts_entries:
                f.write(f"{entry['ip']} {' '.join(entry['domains'])}\n")
        subprocess.run(['ipconfig', '/flushdns'], shell=True, capture_output=True)

    def create_widgets(self):
        # Treeview for entries
        self.tree = ttk.Treeview(self, columns=('IP', 'Domains'), show='headings')
        self.tree.heading('IP', text='IP Address')
        self.tree.heading('Domains', text='Domains')
        self.tree.column('IP', width=150)
        self.tree.column('Domains', width=600)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Control buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add Entry", command=self.add_entry).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Edit Entry", command=self.edit_entry).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Entry", command=self.delete_entry).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.destroy).grid(row=0, column=4, padx=5)

        self.refresh_list()

    def refresh_list(self):
        self.load_hosts_file()
        self.tree.delete(*self.tree.get_children())
        for entry in self.hosts_entries:
            self.tree.insert('', 'end', values=(entry['ip'], ', '.join(entry['domains'])))

    def add_entry(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add New Entry")
        
        tk.Label(dialog, text="IP Address:").grid(row=0, column=0, padx=5, pady=5)
        ip_entry = ttk.Entry(dialog)
        ip_entry.grid(row=0, column=1, padx=5, pady=5)
        ip_entry.insert(0, "127.0.0.1")
        
        tk.Label(dialog, text="Domains (space-separated):").grid(row=1, column=0, padx=5, pady=5)
        domains_entry = ttk.Entry(dialog)
        domains_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def save():
            ip = ip_entry.get().strip()
            domains = domains_entry.get().strip().split()
            if ip and domains:
                self.hosts_entries.append({'ip': ip, 'domains': domains})
                self.save_hosts_file()
                self.refresh_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Both IP and Domain(s) are required")
        
        ttk.Button(dialog, text="Save", command=save).grid(row=2, columnspan=2, pady=10)

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an entry to edit")
            return
        
        index = self.tree.index(selected[0])
        entry = self.hosts_entries[index]
        
        dialog = tk.Toplevel(self)
        dialog.title("Edit Entry")
        
        tk.Label(dialog, text="IP Address:").grid(row=0, column=0, padx=5, pady=5)
        ip_entry = ttk.Entry(dialog)
        ip_entry.grid(row=0, column=1, padx=5, pady=5)
        ip_entry.insert(0, entry['ip'])
        
        tk.Label(dialog, text="Domains (space-separated):").grid(row=1, column=0, padx=5, pady=5)
        domains_entry = ttk.Entry(dialog)
        domains_entry.grid(row=1, column=1, padx=5, pady=5)
        domains_entry.insert(0, ' '.join(entry['domains']))
        
        def save():
            ip = ip_entry.get().strip()
            domains = domains_entry.get().strip().split()
            if ip and domains:
                self.hosts_entries[index]['ip'] = ip
                self.hosts_entries[index]['domains'] = domains
                self.save_hosts_file()
                self.refresh_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Both IP and Domain(s) are required")
        
        ttk.Button(dialog, text="Save", command=save).grid(row=2, columnspan=2, pady=10)

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
        
        index = self.tree.index(selected[0])
        del self.hosts_entries[index]
        self.save_hosts_file()
        self.refresh_list()

if __name__ == "__main__":
    app = HostsManager()
    app.mainloop()