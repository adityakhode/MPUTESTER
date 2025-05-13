# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files
import os
from PySide6.QtCore import QLibraryInfo

# 1. Get the actual Qt paths from PySide6
QT_PLUGINS_PATH = QLibraryInfo.path(QLibraryInfo.PluginsPath)
QT_QML_PATH = QLibraryInfo.path(QLibraryInfo.QmlImportsPath)

# 2. Application data files
datas = [
    # Your application files
    ('frontend/v1.ui', 'frontend'),
    ('frontend/assets.qrc', 'frontend'),
    ('frontend/assets/*', 'frontend/assets'),
    ('refrenceMaterial/certificate/*', 'refrenceMaterial/certificate'),

    # Qt files
    (QT_PLUGINS_PATH, 'PySide6/Qt/plugins'),
    (QT_QML_PATH, 'PySide6/Qt/qml'),

    # Additional Qt dependencies
    (os.path.join(QT_PLUGINS_PATH, 'platforms'), 'PySide6/Qt/plugins/platforms'),
    (os.path.join(QT_PLUGINS_PATH, 'imageformats'), 'PySide6/Qt/plugins/imageformats'),
]

# 3. Additional binaries if needed
binaries = []

# 4. Hidden imports
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtNetwork',
    'pandas',
    'openpyxl',
    'sqlite3',
    'pkg_resources.py2_warn'
]

a = Analysis(
    ['app.py'],
    pathex=[os.getcwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MPUTester',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)