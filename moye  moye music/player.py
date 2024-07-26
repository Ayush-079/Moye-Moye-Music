import os
import requests
from youtubesearchpython import VideosSearch
from pytube import YouTube
import io
from pydub import AudioSegment
import data_handel as dh
import pygame

def search(query, max_results=6):
    videos_search = VideosSearch(query, limit=max_results)
    result = videos_search.result()
    videos = [result['result'][i]['link'] for i in range(0, 6)]
    return videos

def get_audio_and_thumbnail_urls(video_url):
    try:
        yt = YouTube(video_url)
        duration = yt.length
        title = yt.title
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_url = audio_stream.url
        thumbnail_url = yt.thumbnail_url
        return audio_url, thumbnail_url, duration, title
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None
def fetch(song_):
    try:
        
        song = song_ + " song"
        song_url = search(song)[0]
        audio_url, thumbnail_url, duration_seconds, title = get_audio_and_thumbnail_urls(song_url)
        try:
            os.makedirs("C:/songs/")
        except:
            pass
        audio_stream = YouTube(song_url).streams.filter(only_audio=True).first()
        audio_stream.download(filename=f'{song_}.m4a', output_path="C:/songs/")
        m4a_file = f'C:/songs/{song_}.m4a'
        mp3_filename = f'C:/songs/{song_}.mp3'
        thumb_ = requests.get(thumbnail_url)
        thumb_path = f"C:/songs/{song_}.jpg"
        with open(f"C:/songs/{song_}.jpg", "wb") as t:
            t.write(thumb_.content)
            print('downloaded thumbnail image')
        sound = AudioSegment.from_file(m4a_file, format='m4a')
        sound.export(mp3_filename, format='mp3')
        print('mp3 download success')
        print("pushing into database")
        dh.push(title.lower(), duration_seconds, f"C:/songs/{song_}.mp3", f"C:/songs/{song_}.jpg")
        print("pushed into database")
        os.system(f"del {thumb_path.replace('/', '\\')}")
        os.system(f"del {mp3_filename.replace('/', '\\')}")
    except Exception as e:
        print(e)
    return song_url, song_, thumbnail_url, duration_seconds

class Player:
    def __init__(self, song, loops=0):
        self.song = song
        self.loops = loops
        audio_blob = dh.get(self.song)[0]
        audio_file = io.BytesIO(audio_blob)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)

    def play(self):
        pygame.mixer.music.play(loops=self.loops)

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()
    