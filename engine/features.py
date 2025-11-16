from playsound import playsound
import eel
from engine.config import ASSISTANT_NAME
import os
from engine.command import speak
import sqlite3
import webbrowser
from hugchat import hugchat

con=sqlite3.connect('Prajñāvan.db')
cursor=con.cursor()


#Playing Assistant Sound Function
@eel.expose
def playAssistantSound():
    music_dir="www\\assets\\audio\\AV starting_audio.mp3"
    playsound(music_dir)
    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()
    # normalize input correctly (assign lower() result)
    q = (query or "")
    q = q.replace(ASSISTANT_NAME, "")
    q = q.replace("open", "")
    q = q.lower().strip()
    app_name = q


    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")
            

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\huggingface_cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
       