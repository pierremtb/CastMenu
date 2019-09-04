import pychromecast

class StatusMediaListener:
    def __init__(self, callback):
        self.callback = callback
    
    def new_media_status(self, status):
        self.callback(status)

class Device(object):
    
    volume_offset = 0.01

    def __init__(self, app):
        self.app = app

        self.connect()
        

    def connect(self):
        # self.app.title = f"Connecting to {self.app.deviceName}…"
        self.app.title = ""

        self.app.chromecasts = pychromecast.get_chromecasts()
        potentialSpeakers = [cc for cc in self.app.chromecasts if cc.device.friendly_name == self.app.deviceName]

        if len(potentialSpeakers) == 0:
            exc = f"Can't find {self.app.deviceName}"
            print(exc)
            raise Exception(exc)

        self.speaker = potentialSpeakers[0]
        self.speaker.wait()
        print(self.speaker.status)
        print("\nREADY!\n")
        # self.app.title = f"Connected to {self.app.deviceName}!"

        self.previous_volume = self.__getVolume()
        listener = StatusMediaListener(self.__onMediaChanged)
        self.speaker.media_controller.register_status_listener(listener)

    def sendAction(self, action):
        try:
            action()
        except:
            self.connect()
            action()

    def __onMediaChanged(self, status):
        volume = int(self.__getVolume() * 100)
        if status.artist != None and status.title != None:
            title = f"{status.artist} > {status.title}"
        self.app.updateData(self.app.deviceName, title, status.player_is_paused, volume)

    def __setVolume(self, volume):
        self.sendAction(lambda: self.speaker.set_volume(volume))
        print(f"New volume: {int(volume * 100)}%")

    def __getVolume(self):
        return self.speaker.status.volume_level

    def toggleMute(self):
        if self.__getVolume() == 0.0:
            self.__setVolume(self.previous_volume)
            return
        self.previous_volume = self.__getVolume()
        self.__setVolume(0.0)

    def volumeUp(self):
        self.__setVolume(self.__getVolume() + self.volume_offset)

    def volumeDown(self):
        self.__setVolume(self.__getVolume() - self.volume_offset)

    def setVolume(self, volumePercent):
        self.__setVolume(volumePercent / 100)

    def togglePlay(self):
        if self.speaker.media_controller.status.player_is_playing:
            self.sendAction(lambda: self.speaker.media_controller.pause())
            self.previous_playing_state = False
            print("Pause")
            return
        self.sendAction(lambda: self.speaker.media_controller.play())
        self.previous_playing_state = True
        print("Play")

    def next(self):
        self.sendAction(lambda: self.speaker.media_controller.queue_next())
        print("Next")

    def previous(self):
        self.sendAction(lambda: self.speaker.media_controller.queue_prev())
        print("Previous")