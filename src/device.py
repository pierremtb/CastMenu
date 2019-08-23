import pychromecast

class StatusMediaListener:
    def __init__(self, callback):
        self.callback = callback
    
    def new_media_status(self, status):
        self.callback(status)

class Device(object):
    
    volume_offset = 0.02

    def __init__(self, deviceName, app):
        self.deviceName = deviceName
        self.app = app

        self.connect()

        self.previous_volume = self.speaker.status.volume_level
        listener = StatusMediaListener(self.__onMediaChanged)
        self.speaker.media_controller.register_status_listener(listener)

    def connect(self):
        chromecasts = pychromecast.get_chromecasts()
        potentialSpeakers = [cc for cc in chromecasts if cc.device.friendly_name == self.deviceName]

        if len(potentialSpeakers) == 0:
            print("Can't find your device. Quitting...")
            exit(0)

        self.speaker = potentialSpeakers[0]
        self.speaker.wait()
        print(self.speaker.status)
        print("\nREADY!\n")
        self.app.title = f"Connected to {self.deviceName}!"

    def __onMediaChanged(self, status):
        volume = int(self.__getVolume() * 100)
        title = f"{status.artist} — {status.title}"
        playButtonText = "Pause"
        if status.player_is_paused:
            title += " (:)"
            playButtonText = "Play"
        self.app.updateData(self.deviceName, title, playButtonText, volume)

    def __setVolume(self, volume):
        self.speaker.set_volume(volume)
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
            self.speaker.media_controller.pause()
            self.previous_playing_state = False
            print("Pause")
            return
        self.speaker.media_controller.play()
        self.previous_playing_state = True
        print("Play")

    def next(self):
        self.speaker.media_controller.queue_next()
        print("Next")

    def previous(self):
        self.speaker.media_controller.queue_prev()
        print("Previous")