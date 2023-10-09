from pynput import mouse, keyboard
from pynput.keyboard import Controller 
import threading
import logging
import openai
import time
import pyautogui
import creds

k = Controller()

# GPT Token
openaitoken = creds.openai_token()

# Import Library
import tkinter as tk
from tkinter import *

# Create Object
root = Tk()

# Set title
root.title("Main Window")

# Set Geometry
root.geometry("200x200")
text = tk.StringVar()

class ChatGPT3(object):
    def __init__(self, config=None):
        if config is None:
            config = {"model": "text-davinci-003",
                      "context": ""}
        self.openai_api_key = openaitoken
        self.model = config['model']
        self.context = config['context']

    def get_response(self, text):
        openai.api_key = self.openai_api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            temperature=1,
            max_tokens=2000,
            top_p=0.9,
            frequency_penalty=1,
            presence_penalty=0
        )
        return response['choices'][0]['text']

    def chat(self, text):
        response = self.get_response(self.context + text) 
        self.context += text + "\n"
        logging.info(response)
        return response

# Open New Window
def launch():
    global second
    second = Toplevel()
    second.title("LocalizedGPT")
    # setting the windows size
    second.geometry("650x35")
    
    # declaring string variable
    # for storing name and password
    name_var=tk.StringVar()
    
    # defining a function that will
    # get the name and password and
    # print them on the screen
    def submit():
        convo = ChatGPT3()
        text=name_var.get()
        
        print("The text is : " + text)
        second.withdraw()
        time.sleep(1)
        pyautogui.write(convo.chat(text))
            
        
        
        
    name_label = tk.Label(second, text = 'Prompt', font=('calibre',10, 'bold'))
    name_entry = tk.Entry(second,textvariable = name_var, font=('calibre',10,'normal'), width=50)
    sub_btn=tk.Button(second,text = 'Submit', command = submit)
    name_entry.focus()
    
    # placing the label and entry in
    # the required position using grid
    # method
    name_label.grid(row=0,column=0)
    name_entry.grid(row=0,column=1)
    sub_btn.grid(row=0,column=2)

    second.bind("<Return>", (lambda event: submit()))


    

# Show the window
def show():
	second.deiconify()

# Hide the window
def hide():
	second.withdraw()

# Add Buttons
tk.Label(root, text = 'LocalizedGPT', font=('calibre',10, 'bold'))
Button(root, text="launch Window", command=launch).pack(pady=10)
Button(root, text="Show", command=show).pack(pady=10)# Execute Tkinter
Button(root, text="Hide", command=hide).pack(pady=10)



def listen():
    def on_activate():
        print('Global hotkey activated!')
        launch()

    def for_canonical(f):
        return lambda k: f(l.canonical(k))

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<alt>+s'),
        on_activate)
    with keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)) as l:
        l.join()

# Execute Tkinter

x = threading.Thread(target=listen)
x.start()
root.mainloop()


