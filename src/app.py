import rumps

class StatusBarApp(rumps.App):

    def __init__(self, initName):
        super(StatusBarApp, self).__init__(initName)
        self.deviceName = initName

        self.playPauseItem = rumps.MenuItem("Play", callback=lambda _ : self.__onPlayPauseClicked())
        self.volumeDescItem = rumps.MenuItem("Volume")
        self.volumeItem = rumps.SliderMenuItem(value=0, min_value=0, max_value=100, callback=lambda item : self.__onVolumeChanged(item.value))

        self.preferencesItem = rumps.MenuItem("Preferences")
        self.deviceSelectedItem = rumps.MenuItem(f"Device: {self.deviceName}", callback=lambda _ : self.__onDeviceSelectedClicked())
        self.preferencesItem.add(self.deviceSelectedItem)

        self.menu = [self.playPauseItem, self.volumeDescItem, self.volumeItem, None, self.preferencesItem]

    def __onPlayPauseClicked(self):
        self.device.togglePlay()

    def __onDeviceSelectedClicked(self):
        self.window = rumps.Window("Enter the Chromecast-enabled device name:", title="Select Device", default_text=self.deviceName)
        self.window.run()
        self.deviceName = self.window.default_text

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