import os
import queue
import shutil
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import yt_dlp
from PIL import Image, ImageTk


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def find_ffmpeg():
    executable_dir = os.path.dirname(sys.executable)
    candidates = [
        os.path.join(executable_dir, "ffmpeg.exe"),
        resource_path("ffmpeg.exe"),
        shutil.which("ffmpeg"),
    ]
    return next((path for path in candidates if path and os.path.isfile(path)), None)


def update_download_status():
    try:
        while True:
            event, data = download_events.get_nowait()
            if event == "status":
                set_status(data)
            elif event == "success":
                set_status("Download complete.")
                messagebox.showinfo("INFO", data)
                download_button.config(state=tk.NORMAL)
            elif event == "error":
                set_status("Download failed.")
                messagebox.showerror("ERROR", data)
                download_button.config(state=tk.NORMAL)
    except queue.Empty:
        pass
    root.after(100, update_download_status)


def set_status(text):
    status_label.config(text=text)
    if text:
        status_label.place(relx=0.5, rely=0.62, anchor="center")
    else:
        status_label.place_forget()


def download_worker(url, path, fmt):
    ffmpeg_path = find_ffmpeg()
    js_runtimes = {"deno": {}}
    if shutil.which("node"):
        js_runtimes["node"] = {}
    options = {
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "js_runtimes": js_runtimes,
        "progress_hooks": [download_progress],
        "postprocessor_hooks": [download_postprocessor_progress],
        "retries": 3,
        "fragment_retries": 3,
        "socket_timeout": 30,
    }

    if ffmpeg_path:
        options["ffmpeg_location"] = ffmpeg_path

    if fmt == "MP4":
        options.update({
            "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b",
            "merge_output_format": "mp4",
        })
    else:
        if not ffmpeg_path:
            download_events.put((
                "error",
                "FFmpeg could not be found. Reinstall the app or install FFmpeg.",
            ))
            return
        options.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })

    try:
        with yt_dlp.YoutubeDL(options) as downloader:
            info = downloader.extract_info(url, download=True)
        title = info.get("title", "Your video")
        download_events.put(("success", f"Downloaded: {title}"))
    except yt_dlp.utils.DownloadError as error:
        error_text = str(error)
        lowered_error = error_text.casefold()
        if "not a bot" in lowered_error or "bot check" in lowered_error:
            error_text = (
                "YouTube temporarily blocked this request as bot traffic. "
                "Wait a while and try again; repeated requests can prolong "
                "the block.\n\n"
                f"Details: {error_text}"
            )
        download_events.put(("error", error_text))
    except Exception as error:
        download_events.put(("error", f"Unexpected download error: {error}"))


def download_progress(data):
    if data["status"] == "downloading":
        percentage = data.get("_percent_str")
        if percentage:
            status = f"Downloading... {percentage.strip()}"
        else:
            status = "Downloading..."
        download_events.put(("status", status))
    elif data["status"] == "finished":
        download_events.put(("status", "Download received; processing file..."))


def download_postprocessor_progress(data):
    if data["status"] == "started":
        download_events.put(("status", "Converting audio..."))


def download_video():
    url = url_entry.get().strip()
    path = path_entry.get().strip()
    fmt = format_toggle.get()

    if not url:
        messagebox.showerror("Invalid input", "Please enter a video URL.")
        return
    if not path or not os.path.isdir(path):
        messagebox.showerror(
            "Invalid input", "Please choose an existing download folder."
        )
        return

    download_button.config(state=tk.DISABLED)
    set_status("Downloading... PLEASE WAIT")
    threading.Thread(
        target=download_worker,
        args=(url, path, fmt),
        daemon=True,
    ).start()


def choose_directory():
    selected_path = filedialog.askdirectory()
    if selected_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, selected_path)


root = tk.Tk()
root.title("Hipermiklos YTDownloader")
root.geometry("500x500")
root.configure(bg="dark red")

url_label = tk.Label(root, text="URL: ")
url_label.place(relx=0.5, rely=0.05, anchor="center")
url_entry = tk.Entry(root, width=50)
url_entry.place(relx=0.5, rely=0.1, anchor="center")

format_label = tk.Label(root, text="Format: ")
format_label.place(relx=0.5, rely=0.19, anchor="center")


class ToggleSwitch(tk.Frame):
    def __init__(self, master, options, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command = command
        self.options = options
        self.var = tk.StringVar(value=options[0])
        self.buttons = []
        for option in options:
            button = tk.Button(
                self, text=option, relief="raised", bd=2,
                command=lambda opt=option: self.select(opt)
            )
            button.pack(side="left", expand=True, fill="both")
            self.buttons.append(button)
        self.update_buttons()

    def select(self, option):
        self.var.set(option)
        self.update_buttons()
        if self.command:
            self.command(option)

    def update_buttons(self):
        for button in self.buttons:
            if button.cget("text") == self.var.get():
                button.config(relief="sunken", bg="lightgray")
            else:
                button.config(relief="raised", bg="SystemButtonFace")

    def get(self):
        return self.var.get()


format_toggle = ToggleSwitch(root, ["MP4", "MP3"])
format_toggle.place(relx=0.5, rely=0.24, anchor="center")

path_label = tk.Label(root, text="Download path: ")
path_label.place(relx=0.5, rely=0.35, anchor="center")
path_entry = tk.Entry(root, width=50)
path_entry.place(relx=0.5, rely=0.4, anchor="center")
path_entry.insert(0, os.path.expanduser("~/Downloads"))

pathfiledialog = tk.Button(root, text="...", command=choose_directory)
pathfiledialog.place(relx=0.815, rely=0.4, anchor="w")

download_button = tk.Button(
    root, text="Submit", bg="lightgray", command=download_video
)
download_button.place(relx=0.5, rely=0.55, anchor="center")
status_label = tk.Label(root, text="")
status_label.place_forget()

image_path = resource_path("icon.png")
pil_image = Image.open(image_path).resize((100, 100))
img = ImageTk.PhotoImage(pil_image)
image_label = tk.Label(root, image=img, bg="dark red")
image_label.image = img
image_label.place(relx=0.5, rely=1, anchor="s")
root.iconphoto(False, ImageTk.PhotoImage(Image.open(image_path)))

image_text = tk.Label(
    root, text="Hipermiklos Softwares", bg="dark red", fg="white",
    font=("Arial", 12, "bold")
)
image_text.place(relx=0.5, rely=0.8, anchor="s")

download_events = queue.Queue()
root.after(100, update_download_status)
root.mainloop()
