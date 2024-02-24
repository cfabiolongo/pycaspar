import speech_recognition as sr

import os
import sys
import pyaudio

devnull = os.open(os.devnull, os.O_WRONLY)
old_stderr = os.dup(2)
sys.stderr.flush()
os.dup2(devnull, 2)
os.close(devnull)

p = pyaudio.PyAudio()

os.dup2(old_stderr, 2)
os.close(old_stderr)

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

r = sr.Recognizer()
speech = sr.Microphone(device_index=1)
with speech as source:
    print("say something!…")
    audio = r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
try:
    recog = r.recognize_google(audio, language = 'en-US')

    print("You said: " + recog)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))