# voice_qabot.py
# Run with: python voice_qabot.py
# Requirements: pip install SpeechRecognition pyttsx3 pyaudio

import re
import sys
import speech_recognition as sr
import pyttsx3
from difflib import get_close_matches

BOT_NAME = "MUJTABA Assistant"
DEVELOPER = "Mujtaba"

ANSWERS = {
    "whats your name": f"My name is {BOT_NAME}.",
    "what is your name": f"My name is {BOT_NAME}.",
    "who developed you": f"I was developed by {DEVELOPER}.",
    "who built you": f"I was developed by {DEVELOPER}.",
    "who built pakistan": "Pakistan was founded through the efforts of many leaders; its most widely recognised founder is Muhammad Ali Jinnah.",
    "who founded pakistan": "Pakistan's founding leader was Muhammad Ali Jinnah (Quaid-e-Azam).",
    "who is the founder of pakistan": "Muhammad Ali Jinnah is regarded as the founder of Pakistan.",
    "what was the founder of pakistan": "If you mean 'who was the founder of Pakistan' — it's Muhammad Ali Jinnah.",
    "hello": "Hello! Ask me a question.",
    "hi": "Hi there! What do you want to ask?",
    "help": "You can ask questions of any type i always help you",
}

KNOWN_QUESTS = list(ANSWERS.keys())

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def find_answer(user_q: str):
    q = normalize(user_q)
    if q in ANSWERS:
        return ANSWERS[q]
    for key in KNOWN_QUESTS:
        if key in q:
            return ANSWERS[key]
    close = get_close_matches(q, KNOWN_QUESTS, n=1, cutoff=0.6)
    if close:
        return ANSWERS[close[0]]
    if q.startswith("what is your name") or "your name" in q:
        return ANSWERS.get("whats your name")
    if "develop" in q or "built" in q:
        return ANSWERS.get("who developed you")
    if "found" in q and "pakistan" in q:
        return ANSWERS.get("who founded pakistan")
    return "Sorry, I don't know the answer to that yet."

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Say something (or say 'exit' to quit)...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio, language="en")
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Speech recognition service unavailable.")
        return ""

def main():
    print(f"{BOT_NAME} — Voice Q&A Bot (say 'exit' to quit)")
    while True:
        query = listen()
        if not query:
            continue
        if query.lower() in ("exit", "quit", "stop"):
            print("👋 Bye — thanks for chatting!")
            speak("Bye, thanks for chatting!")
            break
        answer = find_answer(query)
        print(f"{BOT_NAME}: {answer}")
        speak(answer)

if __name__ == "__main__":
    main()
