import keyboard
import os
import subprocess
import sys
import platform

from app import CastMenuApp

def _mac_elevate():
    """Relaunch asking for root privileges."""
    print("Relaunching with root permissions")
    # applescript = ('do shell script "python3 ./src/CastMenu.py" '
    #                'with administrator privileges')
    applescript = ('do shell script "../MacOS/CastMenu" '
                   'with administrator privileges')
    exit_code = subprocess.call(['osascript', '-e', applescript])
    sys.exit(exit_code)

def _elevate():
    """Elevate user permissions if needed"""
    if platform.system() == 'Darwin':
        try:
            os.setuid(0)
        except OSError:
            _mac_elevate()

_elevate()
app = CastMenuApp()
app.run()
keyboard.wait()
