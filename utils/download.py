

from pytube import YouTube

# misc
import os
import shutil
import math
import datetime

# plots
import matplotlib.pyplot as plt

# matplotlib inline
# image operation
import cv2

video = yt = YouTube('https://www.youtube.com/watch?v=kJQP7kiw5Fk')

video.streams.all()

video.streams.filter(file_extension='mp4').all()

video.streams.get_by_itag(18).download()
