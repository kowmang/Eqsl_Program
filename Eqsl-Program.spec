# -*- mode: python ; coding: utf-8 -*-

# Die problematischen 'collect_all' Zeilen wurden entfernt.
# PyInstaller wird die PySide6-Abhängigkeiten nun über die Hooks auflösen
# und dabei die 'excludes' Liste korrekt berücksichtigen.

datas = [('gui_data', 'gui_data'), ('database_sql', 'database_sql'), ('scripts', 'scripts'), ('support_data', 'support_data')]
binaries = []
# Wir fügen nur Module hinzu, die NICHT PySide6 sind, aber versteckt importiert werden müssen (wie sqlite3).
hiddenimports = ['sqlite3']


a = Analysis(
    ['eqsl_main_prog.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DExtras',
        'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic',
        'PySide6.Qt3DRender',
        'PySide6.QtAXContainer',
        'PySide6.QtBluetooth',
        'PySide6.QtCharts',
        'PySide6.Concurrent',
        'PySide6.QtDBus',
        'PySide6.QtLocation',
        'PySide6.QtMultimedia',
        'PySide6.QtMultimediaWidgets',
        'PySide6.QtNfc',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtPdf',
        'PySide6.QtPdfWidgets',
        'PySide6.QtQml',
        'PySide6.QtQuick3D',
        'PySide6.QtSensors',
        'PySide6.QtSerialBus',
        'PySide6.QtSerialPort',
        'PySide6.QtSpatialAudio',
        'PySide6.QtTextToSpeech',
        'PySide6.QtWebChannel',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineQuick',
        'PySide6.QtWebEngineWidgets',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Eqsl-Program',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
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
    name='Eqsl-Program',
)