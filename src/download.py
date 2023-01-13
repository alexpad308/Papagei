# -*- coding: utf-8 -*-


# annie ykdl you-get youtube-dl

import you_get
from you_get import common as you_get

link_bilibili = "https://www.bilibili.com/video/BV1PR4y1k7GC/?spm_id_from=333.999.0.0&vd_source=b27f0eda7b19ee54e41aae954255d077"
link_youtube = "https://www.youtube.com/watch?v=YWxwySV-Tr8"

# you_get.main("-i",link_bilibili)
you_get.script_main(link_bilibili)

# Solution of "urllib.error.HTTPError: HTTP Error 410: Gone"
# python -m pip install --upgrade pytube
# python -m pip install git+https://github.com/pytube/pytube
# https://stackoverflow.com/questions/68680322/pytube-urllib-error-httperror-http-error-410-gone

# from pytube import YouTube


# link = "https://www.youtube.com/watch?v=YWxwySV-Tr8"
# yt = YouTube(link)

# streams = yt.streams.all()
#
# # get all audio stream
# audio_streams = [stream for stream in streams if stream.includes_audio_track]
#
# print(streams)
# print(audio_streams)


# video.streams.all()
# video.streams.filter(file_extension='mp4').all()
# video.streams.get_by_itag(18).download()

# Get all available resolution of the video
# resolutions = [stream.resolution for stream in yt.streams.filter(progressive=True, file_extension='mp4')]
# print(resolutions)

# Download the video with the highest resolution
# video = yt.get('mp4', '720p')
# video.download('./video')


# class getVideo(object):
#     def __init__(self, link):
#         self.link = link
#         self.yt = YouTube(self.link)
#         self.video = self.yt.get('mp4', '720p')
#
#     def download(self, path):
#         self.video.download(path)
