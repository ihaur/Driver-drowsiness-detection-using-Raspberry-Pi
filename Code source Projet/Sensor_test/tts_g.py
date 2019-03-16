from gtts import gTTS
import os

tts = gTTS(text="salut" , lang='fr')
tts.save("result.mp3")
os.system("mpg123 result.mp3")


