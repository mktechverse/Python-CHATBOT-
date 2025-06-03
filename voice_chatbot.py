import speech_recognition as sr
import pyttsx3
import json
import random

from fuzzywuzzy import fuzz


#1. Text-To-Speech (Bot Voice)
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

#2. Speech Recognition (User Voice)

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("\n Listening... Bolna shuru karo:")
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source)
    
    try:
        text=recognizer.recognize_google(audio)
        print(f" You said: {text}")
        return text
    except sr.UnknownValueError:
        print(" Could not Understand the audio.")
        return "sorry,Please prompt me lovingly"
    except sr.RequestError:
        print(" Google Api not available.")
        return "Service error"
    
#3.Load responses from json

with open("responses.json",encoding="utf-8") as file:
    responses = json.load(file)

def get_responses(msg):
    msg = msg.lower().strip()
    best_match = "default"
    highest_score = 0

    for key in responses:
        score = fuzz.partial_ratio(msg, key)
        if score > highest_score and score >= 75:  # You can lower or raise this threshold
            best_match = key
            highest_score = score

    return random.choice(responses[best_match])


#4 Main Chat Loop

print("[Voice Chatbot] is active! (say 'exit' to quit)")

while True:
    user_input = listen()
    
    if any(exit_word in user_input.lower() for exit_word in ["exit","quit","band karo"]):
        speak("Bye ! I Loved it.")
        print("chatbot:Bye! I Loved it.")
        break
    
    bot_reply = get_responses(user_input)
    print(f"Chatbot:{bot_reply}")
    speak(bot_reply)