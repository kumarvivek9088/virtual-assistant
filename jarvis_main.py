import pyttsx3

def speakchild(text):
    engine=pyttsx3.init("sapi5")
    voices=engine.getProperty("voices")
    engine.setProperty("voice",voices[0].id)
    rate=engine.getProperty('rate')
    engine.setProperty("rate",rate-30)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    import struct
    import pyaudio
    import pvporcupine
    import speech_recognition as sr
    from pydub.playback import play
    from pydub import AudioSegment
    import google.generativeai as genai
    import os
    # import pyttsx3
    from dotenv import load_dotenv
    import multiprocessing
    from IPython.display import Markdown
    import textwrap
    import markdown
    from bs4 import BeautifulSoup
    from AppOpener import open as Open,close as Close
    import webbrowser
    load_dotenv()
    porcupine=None
    paud=None
    audio_stream=None
    cp = None
    # GOOGLE_API_KEY = "paste your api key"
    GOOGLE_API_KEY = os.environ.get("apikey")
    genai.configure(api_key=GOOGLE_API_KEY)
    def startsound():
        audio=AudioSegment.from_wav("start up sound.wav")
        play(audio)

    def endsound():
        audio=AudioSegment.from_wav("end up sound.wav")
        play(audio)
    
    def speak(text):
        global cp
        print("Jarvis:",text)
        # engine.say(text)
        # engine.runAndWait()
        cp = multiprocessing.Process(target=speakchild,args=(text,))
        cp.start()
        
    def to_text(text):
        text = text.replace('•', '  *')
        md = Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
        html_text = markdown.markdown(md.data)
        text = "".join(BeautifulSoup(html_text,"html.parser").findAll(text=True))
        return text

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    if not os.path.exists('chose.txt'):
        f = open("chose.txt", 'w')
        f.write('0')
        f.close()



    def jarvis_brain(text):
        print(chat.history)
        q = text.split(" ")
        if q[0] == "open":
            if text=='open youtube':
                        webbrowser.open("https://www.youtube.com/")
                        speak("opening youtube")
            else:
                Open(" ".join(q[1::]),match_closest=True)
                speak(f'opening {" ".join(q[1::])}')
        elif q[0] == "close":
            Close(" ".join(q[1::]),match_closest=True)
            speak(f'closing {" ".join(q[1::])}')
        elif text=='play music':
                file=open("chose.txt",'r')
                chose=file.readlines()
                chose=int(chose[0])
                m='e:\\songs'
                song=os.listdir(m)
                length=len(song)
                speak("now music is playing")
                os.startfile(os.path.join(m,song[chose]))
                chose+=1
                file = open("chose.txt",'w')
                file.write(str(chose))
                file.close()
        elif text=='next':
                file=open("chose.txt",'r')
                chose=file.readlines()
                chose=int(chose[0])
                m='e:\\songs'
                song=os.listdir(m)
                length=len(song)
                if chose>=length:
                    speak("no more music to next")
                    speak("i'm playing music from starting")
                    chose=0
                    os.startfile(os.path.join(m,song[chose]))
                else:
                    os.startfile(os.path.join(m,song[chose]))
                    chose+=1
                file = open("chose.txt",'w')
                file.write(str(chose))
                file.close()
        elif text=='stop music':
                speak('ok boss')
                # Close("Media Player",match_closest=True)
                speak("now i stop music")
                # os.system('taskkill /F /FI "WINDOWTITLE eq Movies & Tv" ')
                os.system('taskkill /F /FI "WINDOWTITLE eq Media Player" ')
                
        else:
            response = chat.send_message(text)
            speak(to_text(response.text))


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
                if cp:
                    cp.kill()
                recognize=sr.Recognizer()
                with sr.Microphone() as source:
                    audio=recognize.listen(source)
                    endsound()
                try:
                    query=recognize.recognize_google(audio,language='en-in')
                    print(query)
                    query = str(query).lower()
                    if query != " " and query != "":
                        # cp = multiprocessing.Process(target=jarvis_brain,args=(query,))
                        # cp.start()
                        jarvis_brain(query)
                        
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
