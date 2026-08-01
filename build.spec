import sys

sys.path.insert(0, SPECPATH)

from app.assets import Assets

assets_path = Assets().zip()

analysis = Analysis(
    ("main.py",),
    pathex=(),
    binaries=(),
    datas=((assets_path, "."),),
    hiddenimports=(),
    hookspath=(),
    hooksconfig={},
    runtime_hooks=(),
    excludes=(),
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(analysis.pure, analysis.zipped_data, cipher=None)
exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    (),
    name="Simple Arcade",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=(),
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/images/icon.ico",
)
