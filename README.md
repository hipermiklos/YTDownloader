Hipermiklos YTDownloader

The downloader uses `yt-dlp` and FFmpeg. The Windows installer includes FFmpeg
and YouTube's JavaScript challenge scripts. If Deno or Node.js is already
installed, the app detects it for YouTube extraction; neither runtime is bundled.

Run `Hipermiklos_YTDownloader_Setup.exe` to install the app and add a Start Menu
shortcut under `Program Files\Hipermiklos_Softwares\YTDownloader`. The installer
copies the unpacked application folder, and can also create a desktop shortcut.
If YouTube temporarily blocks a request, wait before trying again. The app does
not access browser cookies or require a YouTube sign-in.

For local development:

```text
python -m pip install -r requirements.txt
.\build_installer.ps1
```

The installer build requires FFmpeg on `PATH` and Inno Setup 6. Install the
Python dependencies first, then run the script to build the unpacked app and
installer in `dist` and `dist\installer`.

Please always download the software from the releases tab.
