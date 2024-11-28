import os
import sys
from pathlib import Path
from tkinter import filedialog
from yt_dlp import YoutubeDL
import threading
from user_interface import ZypherApp

# Default Downloads folder
download_folder = str(Path.home() / "Downloads")
is_video = True

def changefolder():
    """Change the folder where you'd like to save the video."""
    global download_folder
    download_folder = filedialog.askdirectory()

def changeformat():
    """Toggle between video and audio download formats."""
    global is_video
    is_video = not is_video

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def videodownloader(link, app):
    """Download video or audio from the provided link."""
    if not link:
        app.update_feedback("Please enter a link.", "red")
        return

    def download_thread():
        """Download video in a separate thread."""
        app.start_loading()  # Start loading animation

        if is_video:
            options = {
                'format': 'bestvideo[ext=mp4][height>=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(download_folder, '%(title)s.mp4'),
                'noplaylist': True,
                'nocheckcertificate': True
            }
        else:
            options = {
                'format': 'bestaudio',
                'outtmpl': os.path.join(download_folder, '%(title)s.mp3'),
                'noplaylist': True,
                'nocheckcertificate': True,
                'extract_audio': True,
                'audio_quality': '192K'
            }

        try:
            with YoutubeDL(options) as ydl:
                ydl.download([link])  # Download content
            app.update_feedback("Downloaded!\nCheck your Downloads folder.", "green")
        except Exception as e:
            app.update_feedback("Download error!\nCheck your connection.", "red")
            print(f"Error: {e}")
        finally:
            app.stop_loading()  # Stop loading animation

    # Start the download in a separate thread
    thread = threading.Thread(target=download_thread)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    icon_path = resource_path("resources/video.ico")
    app = ZypherApp(videodownloader, changeformat, icon_path, changefolder)
    app.run()
