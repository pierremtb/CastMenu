import keyboard
import pychromecast

from app import StatusBarApp
from device import Device

config = {
	"DEVICE_NAME": "Desk Speaker",
	"PREV_KEY": "f15",
	"PLAY_KEY": "f16",
	"NEXT_KEY": "f17",
	"MUTE_KEY": "f18",
	"VOLD_KEY": "f19",
	"VOLU_KEY": "f20"
}

if __name__ == '__main__':
    app = StatusBarApp(f"Connecting to {config['DEVICE_NAME']}...")
    
    device = Device(config["DEVICE_NAME"], app)
    app.setDevice(device)

    keyboard.add_hotkey(config["PREV_KEY"], lambda: device.previous())
    keyboard.add_hotkey(config["PLAY_KEY"], lambda: device.togglePlay())
    keyboard.add_hotkey(config["NEXT_KEY"], lambda: device.next())
    keyboard.add_hotkey(config["MUTE_KEY"], lambda: device.toggleMute())
    keyboard.add_hotkey(config["VOLD_KEY"], lambda: device.volumeDown())
    keyboard.add_hotkey(config["VOLU_KEY"], lambda: device.volumeUp())

    app.run()
    keyboard.wait()

