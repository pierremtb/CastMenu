import keyboard
import pychromecast

from app import StatusBarApp
from controls import Controls

MY_DEVICE_NAME = "Desk Speaker"

if __name__ == '__main__':
    app = StatusBarApp(f"Connecting to {MY_DEVICE_NAME}...")

    chromecasts = pychromecast.get_chromecasts()
    potentialSpeakers = [cc for cc in chromecasts if cc.device.friendly_name == MY_DEVICE_NAME]

    if len(potentialSpeakers) == 0:
        print("Can't find your device. Quitting...")
        exit(0)

    speaker = potentialSpeakers[0]
    speaker.wait()
    print(speaker.status)
    print("\nREADY!\n")
    app.title = f"Connected to {MY_DEVICE_NAME}!"

    controls = Controls(speaker, app)
    app.setControls(controls)

    keyboard.add_hotkey('f15', lambda: controls.previous())
    keyboard.add_hotkey('f16', lambda: controls.togglePlay())
    keyboard.add_hotkey('f17', lambda: controls.next())

    keyboard.add_hotkey('f18', lambda: controls.toggleMute())
    keyboard.add_hotkey('f19', lambda: controls.volumeDown())
    keyboard.add_hotkey('f20', lambda: controls.volumeUp())

    app.run()
    keyboard.wait()

