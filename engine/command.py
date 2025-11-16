import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):
     text=str(text)
     engine = pyttsx3.init('sapi5')
     voices = engine.getProperty('voices') 
     engine.setProperty('voice', voices[1].id)
     engine.setProperty('rate', 174) 
     eel.DisplayMessage(text)
     engine.say(text)
     eel.receiverText(text)
     engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        

    except Exception as e:
        return ""
    
    return query

@eel.expose
def allCommands(message=1):
    """
    Handles voice (message==1) or typed (message provided) queries.
    Shows interim message, handles open commands, the special identity response,
    or delegates to chatBot for other queries.
    """
    if message == 1:
        query = takecommand()
        print(query)
        try:
            eel.senderText(query)
        except Exception:
            pass
    else:
        query = message
        try:
            eel.senderText(query)
        except Exception:
            pass

    # show interim "wait" message while backend generates the output
    try:
        eel.DisplayMessage("Wait, output generating...")
    except Exception:
        pass

    try:
        qlower = (query or "").lower()
        if "open" in qlower:
            from engine.features import openCommand
            openCommand(query)
            print("open command executed")
        elif any(phrase in qlower for phrase in ("who are you", "tell me about yourself", "tell me about you")):
            # fixed project-specific response
            response = ("Greetings! I am Qwen, a powerful, large-scale language model. While I draw my core architecture and capabilities from the original development by the Tongyi Lab under Alibaba Group, in this setting, I function as the primary AI agent for the Chatbot Project created by Anannay Varshney from B.Tech CSE, 7th Semester,  "
                            "My role here is to process and generate human-like text, utilizing my advanced features like multilingual communication i.e. supporting 100 languages, complex text creation, and analytical reasoning,  "
                            "This project leverages my API to explore practical applications of state-of-the-art AI.Think of me as a high-performance engine customized for Anannay's innovative college submission. How can I assist you today?")
            try:
                eel.receiverText(response)
            except Exception:
                pass
            try:
                speak(response)
            except Exception:
                pass
            print("identity response sent")
        else:
            from engine.features import chatBot
            chatBot(query)
            print("chat bot executed")
    except Exception as e:
        print("some error occurred:", e)
    finally:
        try:
            eel.ShowHood()
        except Exception:
            pass
    return ""


