from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from time import sleep
from pygame import mixer  # Load the popular external library
import platform


class LoopMusic(Thread):
    def __init__(self, music, loops=1, interval=3):
        super(LoopMusic, self).__init__()
        self.audio = music
        self.interval = interval
        self.loops = loops

    def run(self):
        while self.loops >= 1:
            play(self.audio)
            self.loops -= 1
            sleep(self.interval)


class BackgroundMusic:
    def __init__(self, song_name: str, loops=1, interval=3, forever=True):
        self.song_name = song_name
        self.loops = loops
        if forever:
            self.loops = float("inf")
        self.interval = interval
        self.forever_flag = forever

    def run(self):
        if platform.system() == "Windows":
            mixer.init()
            mixer.music.load(self.song_name)
            mixer.music.play(loops=self.loops)

        elif platform.system() == "Linux":
            music = AudioSegment.from_file(self.song_name)
            thread = LoopMusic(music, loops=self.loops, interval=self.interval)
            thread.setDaemon(True)
            thread.start()

    def __enter__(self):
        self.run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
