import keyboard
import pychromecast

from app import CastMenuApp

if __name__ == '__main__':
    app = CastMenuApp()
    app.run()
    keyboard.wait()
