import speech_recognition as sr
import os
from vosk import KaldiRecognizer, Model
import sys
import os
import pyaudio

#Clear console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Crear un reconocedor
r = sr.Recognizer()
r_vosk = sr.Recognizer()

# Load the Vosk model
if not os.path.exists("vosk-model-es-0.42"):  
    print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    sys.exit(1)

model = Model("vosk-model-es-0.42")
recognizer = KaldiRecognizer(model, 16000)

with sr.Microphone() as source:
    print("Running...")
    #r.adjust_for_ambient_noise(source)
    audio = r_vosk.listen(source)

    # Reconocer el audio usando Vosk API
    text = r_vosk.recognize_vosk(audio, language='es')
    print("Oración reconocida: " + text)