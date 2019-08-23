import rumps

class StatusBarApp(rumps.App):

    def __init__(self, initName):
        super(StatusBarApp, self).__init__(initName)

        self.playPauseItem = rumps.MenuItem("Play", callback=lambda _ : self.__onPlayPauseClicked())
        self.volumeDescItem = rumps.MenuItem("Volume")
        self.volumeItem = rumps.SliderMenuItem(value=0, min_value=0, max_value=100, callback=lambda item : self.__onVolumeChanged(item.value))
        self.menu = [self.playPauseItem, self.volumeDescItem, self.volumeItem, "Preferences"]

    def __onPlayPauseClicked(self):
        self.controls.togglePlay()

    def __onMuteClicked(self):
        self.controls.toggleMute()

    def __onVolumeChanged(self, newVolume):
        self.__updateVolumeDesc(int(newVolume))
        self.controls.setVolume(newVolume)

    def __updateVolumeDesc(self, volume):
        self.volumeDescItem.title = f"Volume: {volume}%"

    def setControls(self, controls):
        self.controls = controls

    def updateData(self, title, playButtonText, volume):
        self.title = title
        self.playPauseItem.title = playButtonText
        self.volumeItem.value = volume
        self.__updateVolumeDesc(volume)

    @rumps.clicked("Preferences")
    def prefs(self, _):
        # TODO: implement prefs
        return