import random
import pytube
import os
import wave
from youtubesearchpython import VideosSearch
import time
import tkinter
from statistics import mean
from pydub import AudioSegment
from youtubesearchpython import Search
import audioread
import subprocess
import pygame
from os import path
import songdetective
from pydub import AudioSegment
import random
import csv
pygame.mixer.init()



def choose_song_from_disc(title):
    files = os.listdir("songs")
    
    seedi=random.randint(1, 1000)
    random.seed(time.time() +seedi)
    title = random.choice(files)
    cwd = os.getcwd()
    cwd_song = cwd+"\\songs\\"+title
    return cwd_song


def get_loudest(sound_get):
    sound = AudioSegment.from_file(sound_get, format="wav")
    sound = sound.set_channels(1)
    samples = sound.get_array_of_samples()
    max_amplitude = max(samples)
    min_amplitude = min(samples)
    max_index, max_amplitude = max(enumerate(samples), key=lambda x: x[1])
    time_code = max_index / sound.frame_rate
    time_code = time_code*1000
    return time_code


def cut_song(sound_get):

    sound = AudioSegment.from_file(sound_get, format="wav")
    loudest_moment = get_loudest(sound_get)
    sound_cut = sound[loudest_moment-3000:]
    try:

        sound_cut.export(sound_get, format="wav")
    except:
        return sound_get

    output_name = sound_get
    faded_sound = AudioSegment.from_file(sound_get, format="wav")
    faded_sound = faded_sound.fade_in(duration=1000)
    os.remove(sound_get)
    faded_sound.export(output_name, format="wav")

    return output_name


for i in range(5):

    title = ""
    composer = ""
    new_file = []
    song_list = []
    start = time.perf_counter()


    title = choose_song_from_disc(title)
    title = title[title.rfind("\\")+1:]
    path_title = "songs\\"+title
    title = title[:-4]


    print("pesem prenesena")
    # izreže do najglasnejšega dela

    pygame.mixer.music.load(cut_song(path_title))
    pygame.mixer.music.play()


    end = time.perf_counter()
    elapsed = end - start


    guess = input("Ugani pesem: ")
    
    try:
        videosSearch = VideosSearch(guess, limit=1)
        guess = videosSearch.result()["result"][0]["title"]
    except:
        pass

    videosSearch = VideosSearch(title, limit=1)
    yt_release_date = videosSearch.result()["result"][0]["publishedTime"]
    title = videosSearch.result()["result"][0]["title"]

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    try:
        guess_edit=guess.lower().split("-")[0]
    except:
        guess_edit=guess.lower()

    if guess.lower() == title.lower() or guess in title.lower():
        print("Pravilno", title)
    else:
        print("Napačno!")
        print("Pravilno je bilo: ", title)
        

    print('Elapsed time:', elapsed)
