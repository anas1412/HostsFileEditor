import PyInstaller.__main__
import os
import sys

# Get the current directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Define icon path
icon_file = os.path.join(base_dir, 'icon.ico')

# Check if icon file exists, if not create it
if not os.path.exists(icon_file):
    try:
        from icon import create_icon_image
        img = create_icon_image()
        img.save(icon_file)
    except Exception as e:
        # If there's an error creating the icon, create a simple one directly
        from PIL import Image, ImageDraw
        img = Image.new('RGBA', (64, 64), color=(0, 120, 212, 255))
        draw = ImageDraw.Draw(img)
        # Draw a simple hosts file icon
        draw.rectangle([10, 10, 54, 54], fill=(255, 255, 255))
        draw.rectangle([16, 20, 48, 22], fill=(0, 0, 0))
        draw.rectangle([16, 28, 48, 30], fill=(0, 0, 0))
        draw.rectangle([16, 36, 48, 38], fill=(0, 0, 0))
        draw.rectangle([16, 44, 48, 46], fill=(0, 0, 0))
        img.save(icon_file)

# Define PyInstaller arguments
pyinstaller_args = [
    'main.py',                          # Script to package
    '--name=HostsFileManager',          # Name of the executable
    '--onefile',                        # Create a single executable file
    f'--icon={icon_file}',              # Icon for the executable
    '--windowed',                       # Don't show console window
    '--uac-admin',                      # Request admin privileges
    '--add-data=icon.py;.',             # Include icon.py file
    '--hidden-import=PIL',              # Include PIL dependency
    '--hidden-import=PIL.Image',        # Include PIL.Image dependency
    '--hidden-import=PIL.ImageDraw',    # Include PIL.ImageDraw dependency
    '--clean',                          # Clean PyInstaller cache
]

# Run PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print("\nBuild completed! Executable can be found in the 'dist' folder.")
print("Note: The application requires administrator privileges to run.")