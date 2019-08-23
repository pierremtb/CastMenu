class StatusMediaListener:
    def __init__(self, callback):
        self.callback = callback

    def new_media_status(self, status):
        self.callback(status)

class Controls(object):
    def __init__(self, speaker, app):
        self.previous_volume = speaker.status.volume_level
        self.volume_offset = 0.02
        self.speaker = speaker
        self.app = app

        listener = StatusMediaListener(self.__onMediaChanged)
        speaker.media_controller.register_status_listener(listener)

    def __onMediaChanged(self, status):
        volume = int(self.__getVolume() * 100)
        title = f"{status.artist} — {status.title}"
        playButtonText = "Pause"
        if status.player_is_paused:
            title += " (:)"
            playButtonText = "Play"
        self.app.updateData(title, playButtonText, volume)

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