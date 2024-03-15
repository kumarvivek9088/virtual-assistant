
import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
from pydub.playback import play
from pydub import AudioSegment
import google.generativeai as genai
import os
import pyttsx3
from dotenv import load_dotenv
load_dotenv()
porcupine=None
paud=None
audio_stream=None
# GOOGLE_API_KEY = "paste your api key"
GOOGLE_API_KEY = os.environ.get("apikey")
genai.configure(api_key=GOOGLE_API_KEY)
def startsound():
    audio=AudioSegment.from_wav("start up sound.wav")
    play(audio)

def endsound():
    audio=AudioSegment.from_wav("end up sound.wav")
    play(audio)
engine=pyttsx3.init("sapi5")
voices=engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
rate=engine.getProperty('rate')
engine.setProperty("rate",rate-30)
def speak(text):
    print("Jarvis:",text)
    engine.say(text)
    engine.runAndWait()
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
try:
    print(pvporcupine.KEYWORDS)
    porcupine=pvporcupine.create(keywords=["jarvis"]) #pvporcupine.KEYWORDS for all keywords
    paud=pyaudio.PyAudio()
    audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
    while True:
        keyword=audio_stream.read(porcupine.frame_length)
        keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)
        keyword_index=porcupine.process(keyword)
        if keyword_index>=0:
            print("hotword detected")
            startsound()
            recognize=sr.Recognizer()
            with sr.Microphone() as source:
                audio=recognize.listen(source)
                endsound()
            try:
                query=recognize.recognize_google(audio,language='en-in')
                print(query)
                query = str(query).lower()
                if query != " " and query != "":
                    response = chat.send_message(query)
                    # print(response.text)
                    speak(response.text)
                    
            except Exception as e:
                pass
                # speak("not recognize")

finally:
    if porcupine is not None:
        porcupine.delete()
    if audio_stream is not None:
        audio_stream.close()
    if paud is not None:
        paud.terminate()
