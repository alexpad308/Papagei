# -*- coding: utf-8 -*-


from pydub import AudioSegment
from pydub.playback import play

class Player(object):
    def __init__(self, filename):
        self.filename = filename
        self.name = self.filename.split('.')[0]
        self.ext = self.filename.split('.')[-1]
        self.audio = AudioSegment.from_mp3(self.filename)

    def play(self):
        play(self.audio)

    def reset(self, filename):
        self.filename = filename
        self.audio = AudioSegment.from_mp3(self.filename)



if __name__ == "__main__":

    file = 'sample_zh.mp3'
    player = Player(file)
    player.play()