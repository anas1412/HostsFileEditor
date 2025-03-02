# Hosts File Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)

A modern, user-friendly GUI application for managing Windows hosts file entries. This tool simplifies the process of viewing, adding, editing, and deleting host entries while maintaining the integrity of your system's hosts file.

## Features

- 🖥️ Clean and intuitive graphical user interface
- ✨ Easy management of hosts file entries
- 🔒 Automatic administrator privilege elevation
- 🔄 Real-time DNS cache flushing
- 📝 Preserves file comments and formatting
- 🎯 Instant preview of changes
- 🛡️ Built-in error handling and validation

## Installation

### Option 1: Run from Source

1. Ensure you have Python 3.6 or higher installed on your system
2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/hostsEditor.git
   cd hostsEditor
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Use Pre-built Executable

If you prefer not to install Python, you can download the pre-built executable from the [Releases](https://github.com/yourusername/hostsEditor/releases) page.

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
   > Note: The application will automatically request administrator privileges as required for hosts file modification.

2. The main interface will display all current hosts file entries in a table format.

3. Use the buttons at the bottom to:
   - **Add Entry**: Create new host entries
   - **Edit Entry**: Modify existing entries
   - **Delete Entry**: Remove unwanted entries
   - **Open File**: View the hosts file in Notepad
   - **Refresh**: Reload entries from the hosts file

## Features in Detail

### Adding Entries
- Click "Add Entry"
- Enter the IP address (default: 127.0.0.1)
- Specify one or more domains (space-separated)
- Click Save to apply changes

### Editing Entries
- Select an entry from the list
- Click "Edit Entry"
- Modify the IP address and/or domains
- Save changes

### Deleting Entries
- Select an entry from the list
- Click "Delete Entry"
- Confirm the deletion

## Building the Executable

To build a standalone executable:

1. Ensure you have all dependencies installed:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller pillow
   ```

2. Run the build script:
   ```bash
   python build_exe.py
   ```

3. Once completed, find the executable in the `dist` folder.

The build script will:
- Create an icon for the application if one doesn't exist
- Package all necessary dependencies
- Configure the executable to request admin privileges automatically
- Create a single-file executable for easy distribution

## Technical Details

- Built with Python's tkinter library for the GUI
- Automatically handles file permissions and administrator privileges
- Preserves hosts file comments and formatting
- Implements real-time DNS cache flushing
- Features error handling and user feedback
- Packaged as a standalone executable using PyInstaller

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python's tkinter library
- Inspired by the need for a modern hosts file management tool
- Thanks to all contributors and users of this project

## Support

If you encounter any problems or have suggestions, please [open an issue](https://github.com/yourusername/hostsEditor/issues) on GitHub.