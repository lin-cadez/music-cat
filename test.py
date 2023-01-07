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
pygame.mixer.init()

def song_dl(title):

    title=str(title.replace("“", "").replace("”", "")).strip()
    print(title)
    cwd = f"{os.getcwd()}\\songs" 
    song=title+".mp3"
    song_out=title+".wav"
    cwd_song=cwd+"\\"+song
    cwd_song_new=cwd+"\\"+song_out
    if os.path.exists(cwd_song_new):
        return cwd_song_new
    else:
        
        url = Search(title, limit = 1)
        url=url.result()["result"][0]["link"]
        
        
        yt = pytube.YouTube(url).streams.filter(only_audio=True).first()
        a=yt.download(filename=song, output_path=cwd)
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
    time_code=time_code*1000-5000
    return time_code

title=""
composer=""
new_file=[]

start = time.perf_counter()#####

file=open("src/pop.txt", "r", encoding="utf-8")
file=file.read().strip().split("\n")
title=random.choice(file).split("---")[1]

sound_get = song_dl(title)
sound = AudioSegment.from_file(sound_get, format="wav")
new_cut = sound[get_loudest(sound_get):]
new_cut.export(sound_get, format="wav")
faded_sound = sound.fade_in(duration=1000)
faded_sound.export(sound_get, format="wav")


pygame.mixer.music.load(sound_get)
pygame.mixer.music.play()


end = time.perf_counter()######
elapsed = end - start
print('Elapsed time:', elapsed)

time.sleep(20)





