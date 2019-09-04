from setuptools import setup

APP = ['src/CastMenu.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'CFBundleIdentifier': 'com.pierrejacquier.castmenu',
        'CFBundleGetInfoString': 'CastMenu. Control your Chromecast-enabled devices from the macOS Menu.',
        'CFBundleDisplayName': 'CastMenu',
    },
    'packages': ['rumps', 'keyboard', 'pychromecast'],
    'iconfile': 'icon.icns',
    'resources': ['src/icons/cast_connected.png', 'src/icons/cast_disconnected.png'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)