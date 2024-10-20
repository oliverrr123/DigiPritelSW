import os
import requests
from pydub import AudioSegment
import pyaudio
import nltk
import ssl
import speech_recognition as sr
from gtts import gTTS
from multiprocessing import Process, Queue
import math
from nltk.stem import WordNetLemmatizer
import random
from flask import Flask, render_template

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
import assets.config as config

lemmatizer = WordNetLemmatizer()

r = sr.Recognizer()


talking = False

running = True

# text = {
#     "content": "Hello, World!!!"
# }

# url = "http://127.0.0.1:5000/update"

# response = requests.post(url, json=text)

# print(f"Response: {response.json()}")

text = {'content': 'hello'}
url = 'http://127.0.0.1:5000/updatestate'
response = requests.post(url, json=text)
print(response.json())

def updateState(text):
    text = {'content': text}
    url = 'http://127.0.0.1:5000/updatestate'
    requests.post(url, json=text)
    # return text

current_slider_value = 50

# def check_slider(slider_value):
#     global current_slider_value
#     print("--------------------")
#     print(f"Slider Value: {slider_value}")
#     print("--------------------")
#     os.system(f'osascript -e "set volume output volume {slider_value}"')
#     if current_slider_value != slider_value:
#         current_slider_value = slider_value
#         print(f"Slider Value: {slider_value}")
#     return 200

def kripl2(talking_queue):
    global running
    global talking
    global current_slider_value
    global slider_value
    while running:
        if not talking_queue.empty():
            talking = talking_queue.get()
            print(talking)

        # print(slider_value)
        # if slider_value != current_slider_value:
        #     print(f"Slider Value: {slider_value}")
        #     current_slider_value = slider_value

    


device = sr.Microphone(device_index=1)
def voice_command_processor(talking_queue, ask=False):
    device = sr.Microphone(device_index=1)
    with device as source:
        if ask:
            audio_playback("What's your command?", talking_queue)
        print('LISTENING')
        updateState('Listening')
        audio = r.listen(source, phrase_time_limit=4)  # Listen to the microphone
        print('WAITING')
        updateState('Waiting')
        updateState('TTS start')
        text = ''  # Preset for the spoken phrase
        try:
            text = r.recognize_google(audio, language='cs')  # Convert speech to text
        except:
            print('Didnt understand')
            # audio_playback('Pardon, můžete to prosím zopakovat?', talking_queue)
            text=''
        if text == '':  # If it's silent, AI will ignore
            print('')
        else:
            print(f"User: {text}")  # Display the spoken phrase
        updateState("TTS stop")
        return text.lower()

def audio_playback(text, talking_queue):
    language = 'cs'#jazyk hlasové výslovnosti
    voice = gTTS(text=text, lang=language) #vytvoření hlasového modelu
    updateState(1)
    voice.save("Voice.mp3") # uložení hlasového modelu
    #updateState(2)
    #sound = AudioSegment.from_mp3('Voice.mp3')
    #updateState(3)
    #sound.export('Voice.wav', format='wav')
    print('TALKING')
    updateState('Talking')
    talking_queue.put(True)
    os.system('ffplay -v 0 -nodisp -autoexit Voice.mp3')
    talking_queue.put(False)
    print(text)

memory = []

def get_response(message):
    url = 'https://api.aivanna.xyz/api/v1/text'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'aivanna-Hr5RNVdhGju0TZXmv0jc0tmJo2Y876seqlJ5QX71NLl48xslex'
    }
    data = {
        'messages': [
            {'role': 'user', 'content': 'Jsi hlasový asistent pro seniory, který má za úkol pomoci s každodenními úkoly. Pokud se tě senior zeptá na něco ohledně technologií a nebudeš vědět, odpověz pouze nevím.'},
            {'role': 'user', 'content': message}
        ],
        'model': 'digi-pritel'
    }
    
    updateState("AI start")
    
    response = requests.post(url, headers=headers, json=data)
    
    print(response.json())
    return response.json()['message']
    
    #response = client.chat.completions.create(
    #    model="gpt-3.5-turbo",
    #    messages=[
    #        {"role": "system", "content": "Jsi hlasový asistent pro seniory, který má za úkol pomoci s každodenními úkoly. Pokud se tě senior zeptá na něco ohledně technologií a nebudeš vědět, odpověz pouze nevím."},
    #        {"role": "user", "content": message},
    #    ]
    #)
    #return response.choices[0].message.content



def execute_voice_command(text, talking_queue): #zařizuje možnost odpovědí hlasem
    if text == '':
        pass
    else:
        message = text
        #intents = predict_class(message)
        response = get_response(message)
        updateState("AI stop")
        audio_playback(response, talking_queue)



def kripl(talking_queue):
    while True:
        if config.VOICE == True:
            command = voice_command_processor(talking_queue)
            execute_voice_command(command, talking_queue)
        elif config.VOICE == False:
            message = input('[?] >> ')
            response = get_response(message)
        else:
            print('voice_command_processor isnt definied')
    

if __name__ == '__main__':
    talking_queue = Queue()

    p1 = Process(target=kripl, args=(talking_queue,))
    p2 = Process(target=kripl2, args=(talking_queue,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
