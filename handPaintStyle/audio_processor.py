from moviepy.editor import *

videoclip_1 = VideoFileClip("zhongli-pv.flv")
videoclip_2 = VideoFileClip("output.flv")

audio_1 = videoclip_1.audio
videoclip_3 = videoclip_2.set_audio(audio_1)

videoclip_3.write_videofile("zhongli-pv-handified.flv", codec="libx264")
