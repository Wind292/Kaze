from pathlib import Path
import pyhandbreak

directory_path = Path(r'C:\Users\jp3\Videos\Valorant')  # Replace with your directory path

for file_path in directory_path.iterdir():
    if file_path.is_file():  # Check if it's a file
        pyhandbreak.formatvid(str(file_path.parent), "wind", bitrate=5000, framerate=60, id=file_path.name)