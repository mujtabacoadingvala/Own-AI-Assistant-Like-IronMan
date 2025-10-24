import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set voice and speaking rate
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # You can change [0] to [1] for a female voice
engine.setProperty('rate', 170)

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's voice and convert to text"""
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("🧠 Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"👉 You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Sorry, I didn't catch that.")
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("⚠️ Speech service unavailable.")
            speak("Speech service is unavailable.")
            return ""

# Main loop
if __name__ == "__main__":
    speak("Hello! I am your talking assistant. Say something.")
    while True:
        command = listen().lower()
        if command == "":
            continue
        elif "stop" in command or "exit" in command or "quit" in command:
            speak("Goodbye!")
            print("👋 Exiting...")
            break
        else:
            print(f"💬 You said: {command}")
            speak(f"You said {command}")
