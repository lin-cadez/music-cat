import random
import pytube
import os
import wave
import pydub
import time
import tkinter
import audioread
import subprocess
import pygame
from os import path
from pydub import AudioSegment
import random

def duration_detector(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds
  
    return hours, mins, seconds
  
def get_length(song):

    with audioread.audio_open(song) as f:
        totalsec = f.duration
        totalsec=totalsec/2
        return float(totalsec)

def get_song():
    file=open("song_bank.txt", "r", encoding="utf-8")
    file=file.read().strip().split("\n")
    song=random.choice(file)
    url = str(song.split("---")[1])
    title = str(song.split("---")[0])
    song=title+".mp3"
    global song_out
    song_out=title+".wav"
    yt = pytube.YouTube(url).streams.filter(only_audio=True).first()
    print(yt)
    a=yt.download(filename=song)
    with open(song, "rb") as f:
        audio_data = f.read()
    subprocess.call(['ffmpeg', '-i', song, song_out])
    os.remove(song)

    return song_out, title


pygame.init()
pygame.mixer.get_init() 





a, b=get_song()  
pygame.mixer.music.load(a)
print("")
print(b)
ch = pygame.mixer.music.play()
time.sleep(50)

    

