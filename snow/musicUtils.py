from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from time import sleep


class LoopMusic(Thread):
    def __init__(self, music, loop=1, forever=False):
        super(LoopMusic, self).__init__()
        self.audio = AudioSegment.from_mp3(music)
        if forever:
            self.loop = float("inf")
        else:
            self.loop = loop

    def run(self):
        while self.loop >= 1:
            play(self.audio)
            self.loop -= 1
            sleep(5)


class BackgroundMusic:
    def __init__(self, song_name: str, forever=True):
        self.thread = LoopMusic(song_name, forever=forever)
        self.thread.setDaemon(True)

    def run(self):
        self.thread.start()

    def __enter__(self):
        self.run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.thread.join()
        pass
