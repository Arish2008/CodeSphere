import speech_recognition as sr
import webbrowser
import pyttsx3
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi ="YOUR_API_KEY" # Note: The API key has been hashed for security reasons. 
# Please replace 'YOUR_API_KEY' with your own key to use this code.

# Function to speak a given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Songs dictionary with song name and YouTube link
songs = {
    "who they": "https://www.youtube.com/watch?v=wBw6Leb5F2U",
    "block": "https://www.youtube.com/watch?v=e4c5i1fyW-4"
}

# Function to process recognized commands
def processword(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split("play ")[1].strip()
        link = songs.get(song, None)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I don't have the song {song}.")
        
    elif "news" in c.lower():
        r=requests.get("YOUR_API_KEY")       #  your news api key will come here
        if r.status_code==200:
            data =r.json()
            articles = data.get("articles",None)
            for article in articles:
                speak(article["title"])
          
# Main logic
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            # Obtain audio from the microphone
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            
            # Recognize the keyword 'Jarvis'
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processword(command)
        
        except Exception as e:
            print(f"Error: {str(e)}")
