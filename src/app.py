import rumps
import json
import os
import keyboard
from device import Device

CONFIG_DIR = os.path.expanduser("~/.castmenu")
CONFIG_NAME = "config.json"
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_NAME)
DEFAULT_CONFIG = {
	"DEVICE_NAME": "Desk Speaker",
	"PREV_KEY": "f15",
	"PLAY_KEY": "f16",
	"NEXT_KEY": "f17",
	"MUTE_KEY": "f18",
	"VOLD_KEY": "f19",
	"VOLU_KEY": "f20"
}
KEY_NAMES = {
	"PREV_KEY": "Previous",
	"PLAY_KEY": "Play/Pause",
	"NEXT_KEY": "Next",
	"MUTE_KEY": "Mute/Unmute",
	"VOLD_KEY": "Volume Down",
	"VOLU_KEY": "Volume Up"
}

class CastMenuApp(rumps.App):

    def __init__(self):
        super(CastMenuApp, self).__init__("", quit_button=None)

        self.config = self.getConfig()

        self.chromecasts = []

        self.deviceName = self.config["DEVICE_NAME"]

        try:
            self.device = Device(self)
            self.setMenu()
            self.setHotkeys()
        except:
            print("hey")
            # self.__onDeviceSelectedClicked()

    def setMenu(self):

        self.playPauseItem = rumps.MenuItem("Play", callback=lambda _: self.__onPlayPauseClicked())
        self.volumeDescItem = rumps.MenuItem("Volume")
        self.volumeItem = rumps.SliderMenuItem(value=0, min_value=0, max_value=100, callback=lambda item: self.__onVolumeChanged(item.value))

        self.preferencesItem = rumps.MenuItem("Preferences")
        self.deviceSelectedItem = rumps.MenuItem(f"Device: {self.deviceName}")
        # self.deviceSelectedItem = rumps.MenuItem(f"Device: {self.deviceName}", callback=lambda _ : self.__onDeviceSelectedClicked())
        for cc in self.chromecasts:
            name = cc.device.friendly_name
            self.deviceSelectedItem.add(rumps.MenuItem(name, callback=self.__onDeviceSelected))
        self.preferencesItem.add(self.deviceSelectedItem)
        self.preferencesItem.add(None)
        for key in ["PREV_KEY", "PLAY_KEY", "NEXT_KEY", "MUTE_KEY", "VOLD_KEY", "VOLU_KEY"]:
            self.preferencesItem.add(rumps.MenuItem(f"{KEY_NAMES[key]}: {self.config[key]}", callback=self.__onKeyClicked))

        self.quitItem = rumps.MenuItem("Quit", callback=lambda item: rumps.quit_application())

        self.menu.clear()
        self.menu = [self.playPauseItem, self.volumeDescItem, self.volumeItem, None, self.preferencesItem, self.quitItem]

    def setHotkeys(self):
        keyboard.add_hotkey(self.config["PREV_KEY"], lambda: self.device.previous())
        keyboard.add_hotkey(self.config["PLAY_KEY"], lambda: self.device.togglePlay())
        keyboard.add_hotkey(self.config["NEXT_KEY"], lambda: self.device.next())
        keyboard.add_hotkey(self.config["MUTE_KEY"], lambda: self.device.toggleMute())
        keyboard.add_hotkey(self.config["VOLD_KEY"], lambda: self.device.volumeDown())
        keyboard.add_hotkey(self.config["VOLU_KEY"], lambda: self.device.volumeUp())

    def __onPlayPauseClicked(self):
        self.device.togglePlay()

    def __onDeviceSelected(self, item):
        self.deviceName = item.title
        self.deviceSelectedItem.title = f"Device: {self.deviceName}"
        self.editConfigKey("DEVICE_NAME", self.deviceName)
        self.__init__()

    def __onKeyClicked(self, item):
        key_name = item.title.split(": ")[0]
        key = next(k for k in KEY_NAMES if KEY_NAMES[k] == key_name)
        self.window = rumps.Window(f"Select key for {KEY_NAMES[key]}", title="Enter the key", default_text=self.config[key])
        res = self.window.run()
        self.editConfigKey(key, res.text)
        self.setMenu()
        self.setHotkeys()

    def __onDeviceSelectedClicked(self):
        print(self.chromecasts)
        availableNames = "\n".join([c.device.friendly_name for c in self.chromecasts])
        message = "Available devices on network:\n" + availableNames
        print(message)
        
        self.window = rumps.Window(message, title="Enter the Chromecast-enabled device name:", default_text=self.deviceName)
        res = self.window.run()
        self.deviceName = res.text
        self.deviceSelectedItem.title = f"Device: {self.deviceName}"
        self.editConfigKey("DEVICE_NAME", self.deviceName)
        self.__init__()

    def __onMuteClicked(self):
        self.device.toggleMute()

    def __onVolumeChanged(self, newVolume):
        self.__updateVolumeDesc(int(newVolume))
        self.device.setVolume(newVolume)

    def __updateVolumeDesc(self, volume):
        self.volumeDescItem.title = f"Volume: {volume}%"

    def setDevice(self, device):
        self.device = device

    def updateData(self, deviceName, title, playButtonText, volume):
        self.deviceName = deviceName
        self.deviceSelectedItem.title = f"Device: {self.deviceName}"
        self.title = title
        self.playPauseItem.title = playButtonText
        self.volumeItem.value = volume
        self.__updateVolumeDesc(volume)

    def editConfigKey(self, key, value):
        self.config[key] = value
        self.saveConfig(self.config)

    def saveConfig(self, config):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f)

    def getConfig(self):
        try:
            f = open(CONFIG_PATH, "rb")
        except IOError:
            print("Creating config file...")
            self.saveConfig(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        
        with f:
            config = json.load(f)
        return config