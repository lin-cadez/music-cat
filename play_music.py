import random
import pytube
import os
import wave
import time
import tkinter
from statistics import mean
from pydub import AudioSegment
from youtubesearchpython import Search
import audioread
import subprocess
import pygame
from os import path
from pydub import AudioSegment
import random
import csv
pygame.mixer.init()

def song_dl(title):

    title=str(title.replace("“", "").replace("”", "")).strip()
    print(title)
    song=title+".mp3"
    song_out=title+".wav"
    cwd = os.getcwd()
    cwd_song=cwd+"\\songs\\"+song
    cwd_song_new=cwd+"\\songs\\"+song_out
    if os.path.exists(cwd_song_new):
        return cwd_song_new
    else:
        
        url = Search(title, limit = 1)
        url=url.result()["result"][0]["link"]
        
        yt = pytube.YouTube(url).streams.filter(only_audio=True).all()[0]
        try:
            a=yt.download(filename=cwd_song)
        except:
            time.sleep(1)
            a=yt.download(filename=cwd_song)
        with open(cwd_song, "rb") as f:
            audio_data = f.read()
        subprocess.call(['ffmpeg', '-i', cwd_song, cwd_song_new])
        os.remove(cwd_song)
        return cwd_song_new

def get_loudest(sound_get):
    sound = AudioSegment.from_file(sound_get, format="wav")
    sound = sound.set_channels(1)
    samples = sound.get_array_of_samples()
    max_amplitude = max(samples)
    min_amplitude = min(samples)
    max_index, max_amplitude = max(enumerate(samples), key=lambda x: x[1])
    time_code = max_index / sound.frame_rate
    time_code=time_code*1000
    return time_code

def cut_song(sound_get):

    sound = AudioSegment.from_file(sound_get, format="wav")
    loudest_moment=get_loudest(sound_get)
    sound_cut = sound[loudest_moment-3000:]
    sound_cut.export(sound_get, format="wav")

    output_name=sound_get
    faded_sound = AudioSegment.from_file(sound_get, format="wav")
    faded_sound = faded_sound.fade_in(duration=1000)
    os.remove(sound_get)
    faded_sound.export(output_name, format="wav")

    return output_name

title=""
composer=""
new_file=[]
song_list=[]
start = time.perf_counter()#####

#izbira pesmi
with open('src/pop.csv', 'r', encoding="utf-8") as file:
  reader = csv.reader(file)

  for row in reader:
    if row!=[]:
        song_list.append(row)

title=random.choice(song_list)
print(title)
title=title[0].split(",")[0]


sound_get = song_dl(title)

#izreže do najglasnejšega dela
pygame.mixer.music.load(cut_song(sound_get))
pygame.mixer.music.play()


end = time.perf_counter()######
elapsed = end - start
print('Elapsed time:', elapsed)

time.sleep(20)

print(sound_get)





