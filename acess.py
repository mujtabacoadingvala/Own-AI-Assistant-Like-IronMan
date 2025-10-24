import webbrowser
import urllib.parse
import speech_recognition as sr
import pyttsx3

# --- Website shortcuts ---
COMMON = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "tiktok": "https://www.tiktok.com",
    "microsoft": "https://www.microsoft.com",
    "twitter": "https://twitter.com",
    "github": "https://github.com",
    "linkedin": "https://www.linkedin.com",
}

# --- Setup speech & voice engine ---
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("🗣️", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎧 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("🧠 Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"👉 You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn’t catch that.")
            return ""
        except sr.RequestError:
            speak("Speech service is unavailable.")
            return ""

def normalize_input(s: str) -> str:
    s = s.strip()
    if not s:
        return ""
    for key in COMMON:
        if key in s:
            return COMMON[key]
    if s.startswith("http://") or s.startswith("https://"):
        return s
    if "." in s and " " not in s:
        return "https://" + s
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(s)

def open_website(url):
    print(f"🌐 Opening: {url}")
    webbrowser.open(url)

def main():
    speak("Hello! Say the name of a website you want to open.")
    while True:
        query = listen()
        if query == "":
            continue
        if "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye!")
            break
        if "open" in query:
            query = query.replace("open", "").strip()
        url = normalize_input(query)
        if url:
            open_website(url)
            speak(f"Opening {query}")
        else:
            speak("Sorry, I couldn’t find that.")

if __name__ == "__main__":
    main()
