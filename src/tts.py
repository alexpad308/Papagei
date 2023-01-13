# -*- coding: utf-8 -*-

# doc: https://pyttsx3.readthedocs.io/en/latest/engine.html

import pyttsx3


def test_TTSX():
    tts = TTSX()

    # change male speaker
    # need to add kangkang.reg to regedit
    if tts.vid.get('kangkang'):
        tts.set_voice('kangkang')

    # change speaker voice
    tts.list_voices()
    for i, voice in enumerate(tts.vid):
        print(i, voice)
        tts.set_voice(voice)
        # print(tts.get_voice())  # get voice

        tts.say("hello world")
        tts.say("春光灿烂猪八戒")
        tts.say("逃げるだけの人生じゃない")

    # reset to default voice
    tts.reset()

    # change speaker speed
    for i in range(3):
        tts.say("小流浪猫趴在窗角整整一下午，弱小可怜又无助。")
        print('speed: ', tts.get_speed())
        tts.add_speed(50)
    tts.reset()

    # change speaker volume
    for i in range(3):
        tts.say("小流浪猫趴在窗角整整一下午，弱小可怜又无助。")
        print('speed: ', tts.get_volume())
        tts.add_volume(-0.4)
    tts.reset()


class TTSX(object):
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)  # 设置语速
        self.engine.setProperty('volume', 0.7)  # 设置音量
        self.voices = self.engine.getProperty('voices')  # 讲述人列表
        self.vid = {}  # 讲述人id列表
        for i, voice in enumerate(self.voices):
            self.vid[voice.name.split(' ')[1].lower()] = i
        self.voice = 'huihui'  # 设置 Huihui 作为讲述人(默认女声)
        self.engine.setProperty('voice', self.voices[self.vid[self.voice]].id)
        self.lang = {'zh-cn': 'huihui', 'en': 'zira'} # 语言对应的讲述人

    def list_voices(self):
        # for i, voice in enumerate(self.voices):
        #     print('id_{} = {} \nname = {} \n'.format(i, voice.id, voice.name))
        print('List of Voices:', self.vid)

    def say(self, text):
        self.engine.say(text, self.voice)
        self.engine.runAndWait()

    def save_to_file(self, text, filename):
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()

    def set_voice(self, voice):
        self.engine.setProperty('voice', self.voices[self.vid[voice]].id)
        self.voice = voice

    def get_voice(self):
        return self.voice

    def set_speed(self, rate):
        self.engine.setProperty('rate', rate)

    def add_speed(self, rate=10):
        rate += self.engine.getProperty('rate')
        self.set_speed(rate)

    def get_speed(self):
        return self.engine.getProperty('rate')

    def set_volume(self, volume):
        volume = 0 if volume < 0 else volume
        volume = 1 if volume > 1 else volume
        self.engine.setProperty('volume', volume)

    def add_volume(self, volume=0.1):
        volume += self.engine.getProperty('volume')
        self.set_volume(volume)

    def get_volume(self):
        return self.engine.getProperty('volume')

    def reset(self):
        self.set_speed(180)
        self.set_volume(0.7)
        self.set_voice('huihui')

    def __del__(self):
        self.engine.stop()


if __name__ == "__main__":
    test_TTSX()
