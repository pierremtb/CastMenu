import rumps
import json
import os
import keyboard
from device import Device

CONFIG_DIR = os.path.expanduser("~/.castmenu")
CONFIG_NAME = "config.json"
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_NAME)
DEFAULT_CONFIG = {
    "DEVICE_NAME": "Chromecast Audio",
    "PREV_KEY": "f15",
    "PLAY_KEY": "f16",
    "NEXT_KEY": "f17",
    "MUTE_KEY": "f18",
    "VOLD_KEY": "f19",
    "VOLU_KEY": "f20",
    "TEXT_SHOWN": True
}
KEY_NAMES = {
    "PREV_KEY": "Previous",
    "PLAY_KEY": "Play/Pause",
    "NEXT_KEY": "Next",
    "MUTE_KEY": "Mute/Unmute",
    "VOLD_KEY": "Volume Down",
    "VOLU_KEY": "Volume Up"
}
# ICONS_PATH = "src/icons"
ICONS_PATH = "."


class CastMenuApp(rumps.App):

    def __init__(self):
        super(CastMenuApp, self).__init__("", quit_button=None)

        self.config = self.getConfig()
        self.__setCastIcon(False)

        self.chromecasts = []
        self.hotkeys = []

        self.deviceName = self.config["DEVICE_NAME"]

        try:
            self.device = Device(self)
            self.setMenu(connected=True)
            self.setHotkeys()
        except:
            self.setMenu(connected=False)
            self.__onDeviceSelectedClicked()

    def __setCastIcon(self, playing=True):
        if playing:
            self.icon = os.path.join(ICONS_PATH, "cast_connected.png")
            return
        self.icon = os.path.join(ICONS_PATH, "cast_disconnected.png")

    def setMenu(self, connected=True):
        self.prevItem = rumps.MenuItem(
            "Previous", callback=lambda _: self.device.previous())
        self.playPauseItem = rumps.MenuItem(
            "Play", callback=lambda _: self.__onPlayPauseClicked())
        self.nextItem = rumps.MenuItem(
            "Next", callback=lambda _: self.device.next())

        self.volumeDescItem = rumps.MenuItem(
            "Volume", callback=lambda _: self.__onMuteClicked())
        self.volumeItem = rumps.SliderMenuItem(
            value=0, min_value=0, max_value=100, callback=lambda item: self.__onVolumeChanged(item.value))

        self.preferencesItem = rumps.MenuItem("Preferences")
        self.deviceSelectedItem = rumps.MenuItem(f"Device: {self.deviceName}")
        self.textShownItem = rumps.MenuItem("Show Artist > Title in Menu Bar", callback=lambda _: self.__onTextShownChanged())
        self.textShownItem.state = int(self.config["TEXT_SHOWN"])
        # self.deviceSelectedItem = rumps.MenuItem(f"Device: {self.deviceName}", callback=lambda _ : self.__onDeviceSelectedClicked())
        for cc in self.chromecasts:
            name = cc.device.friendly_name
            self.deviceSelectedItem.add(rumps.MenuItem(
                name, callback=self.__onDeviceSelected))
        self.preferencesItem.add(self.deviceSelectedItem)
        self.preferencesItem.add(self.textShownItem)
        self.preferencesItem.add(None)
        for key in ["PREV_KEY", "PLAY_KEY", "NEXT_KEY", "MUTE_KEY", "VOLD_KEY", "VOLU_KEY"]:
            self.preferencesItem.add(rumps.MenuItem(
                f"{KEY_NAMES[key]}: {self.config[key]}", callback=self.__onKeyClicked))
        self.preferencesItem.add(None)
        self.reattachKeysItem = rumps.MenuItem(
            "Reload conf", callback=lambda _: self.__init__())
        self.preferencesItem.add(self.reattachKeysItem)

        self.aboutItem = rumps.MenuItem("About", callback=lambda item: os.system(
            "open \"\" https://pierrejacquier.com/castmenu"))
        self.quitItem = rumps.MenuItem(
            "Quit", callback=lambda item: rumps.quit_application())

        self.menu.clear()
        self.menu = [self.prevItem, self.playPauseItem, self.nextItem, None,
                     self.volumeDescItem, self.volumeItem, None,
                     self.preferencesItem, self.aboutItem, self.quitItem]

    def setHotkeys(self):
        for hk in self.hotkeys:
            keyboard.remove_hotkey(hk)
        self.hotkeys.append(keyboard.add_hotkey(
            self.config["PREV_KEY"], lambda: self.device.previous()))
        self.hotkeys.append(keyboard.add_hotkey(
            self.config["PLAY_KEY"], lambda: self.device.togglePlay()))
        self.hotkeys.append(keyboard.add_hotkey(
            self.config["NEXT_KEY"], lambda: self.device.next()))
        self.hotkeys.append(keyboard.add_hotkey(
            self.config["MUTE_KEY"], lambda: self.device.toggleMute()))
        self.hotkeys.append(keyboard.add_hotkey(
            self.config["VOLD_KEY"], lambda: self.device.volumeDown()))
        self.hotkeys.append(keyboard.add_hotkey(
            self.config["VOLU_KEY"], lambda: self.device.volumeUp()))

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
        self.window = rumps.Window(
            f"Select key for {KEY_NAMES[key]}", title="Enter the key", default_text=self.config[key])
        res = self.window.run()
        self.editConfigKey(key, res.text)
        self.setMenu()
        self.setHotkeys()

    def __onDeviceSelectedClicked(self):
        print(self.chromecasts)
        availableNames = "\n".join(
            [c.device.friendly_name for c in self.chromecasts])
        message = "Available devices on network:\n" + availableNames
        print(message)

        self.window = rumps.Window(
            message, title="Enter the Chromecast-enabled device name:", default_text=self.deviceName)
        res = self.window.run()
        self.deviceName = res.text
        self.deviceSelectedItem.title = f"Device: {self.deviceName}"
        self.editConfigKey("DEVICE_NAME", self.deviceName)
        self.__init__()

    def __onMuteClicked(self):
        self.device.toggleMute()

    def __onTextShownChanged(self):
        self.editConfigKey("TEXT_SHOWN", not self.config["TEXT_SHOWN"])
        self.setMenu()

    def __onVolumeChanged(self, newVolume):
        self.__updateVolumeDesc(int(newVolume))
        self.device.setVolume(newVolume)

    def __updateVolumeDesc(self, volume):
        self.volumeDescItem.title = f"Volume: {volume}%"

    def setDevice(self, device):
        self.device = device

    def updateData(self, deviceName, title, playerIsPaused, volume):
        playButtonText = "Pause"
        if playerIsPaused:
            title += " (:)"
            playButtonText = "Play"
        self.deviceName = deviceName
        self.deviceSelectedItem.title = f"Device: {self.deviceName}"
        self.playPauseItem.title = playButtonText
        self.volumeItem.value = volume
        self.__updateVolumeDesc(volume)
        if title != None:
            self.title = title
        self.__setCastIcon(playing=title != None)

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
