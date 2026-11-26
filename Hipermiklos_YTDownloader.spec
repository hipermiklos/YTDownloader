import os
import shutil

from PyInstaller.utils.hooks import collect_submodules

ffmpeg_path = shutil.which("ffmpeg")
if not ffmpeg_path:
    raise RuntimeError("FFmpeg must be installed and available on PATH to build")

a = Analysis(
    ['Hipermiklos_YTDownloader.py'],
    pathex=[],
    binaries=[(ffmpeg_path, '.')],
    datas=[('icon.png', '.'), ('icon.ico', '.')],
    hiddenimports=collect_submodules('yt_dlp'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Hipermiklos_YTDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    icon='icon.ico',
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Hipermiklos_YTDownloader',
)
