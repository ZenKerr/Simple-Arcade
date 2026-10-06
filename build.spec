import sys
import tomllib

from pyinstaller_versionfile import create_versionfile

sys.path.insert(0, SPECPATH)

from app.services.assets import Assets

with open("pyproject.toml", "rb") as project_information_file:
    project_information = tomllib.load(project_information_file)["project"]

name = project_information["name"]
product_name = " ".join(part.capitalize() for part in name.split("_"))
author = project_information["authors"][0]["name"]
versionfile_path = "build/versionfile.txt"

create_versionfile(
    output_file=versionfile_path,
    version=project_information["version"],
    company_name=author,
    file_description=project_information["description"],
    internal_name=name,
    legal_copyright=f"Copyright © 2026 {author}",
    original_filename=f"{product_name}.exe",
    product_name=product_name,
)

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
    name=product_name,
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
    version=versionfile_path,
)
