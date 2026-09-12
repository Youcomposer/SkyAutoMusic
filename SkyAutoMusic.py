import pydirectinput
import time
import threading
import os
from tkinter import Tk, filedialog, Button, Scale, Label, HORIZONTAL, Frame

# Key replacement dictionary
KEY_MAP = {
    "A1": "y", "A2": "u", "A3": "i", "A4": "o", "A5": "p",
    "B1": "h", "B2": "j", "B3": "k", "B4": "l", "B5": "ñ",
    "C1": "n", "C2": "m", "C3": ",", "C4": ".", "C5": "-",
    ".": "1"
}

filename = None

def replace_sent(sentence):
    for old, new in KEY_MAP.items():
        sentence = sentence.replace(old, new)
    return sentence

def press_keys(keys):
    def press_key(key):
        pydirectinput.keyDown(key)
        time.sleep(0.1)
        pydirectinput.keyUp(key)

    threads = []
    for key in keys:
        thread = threading.Thread(target=press_key, args=(key,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def start_process(slider_value):
    global filename
    root.destroy()  
    with open(filename, "r") as file:
        original = file.read().strip()
    modified = replace_sent(original)
    time.sleep(2) 

    
    speed = slider_value  

    group_chars = ''
    for char in modified:
        if char == ' ':
            if group_chars:
                threading.Thread(target=press_keys, args=(list(group_chars),)).start()
                time.sleep(speed)  
                group_chars = ''
            else:
                time.sleep(0.3)  
        else:
            group_chars += char

    if group_chars:
        threading.Thread(target=press_keys, args=(list(group_chars),)).start()

# GUI setup
root = Tk()
root.title("Music AutoPlayer PC")
root.geometry("400x250") 

try:
    icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icon.ico")
    root.iconbitmap(icon_path)
except Exception:
    pass

def choose_file():
    global filename
    initial_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Songs")
    filename = filedialog.askopenfilename(title="Select a file", initialdir=initial_dir,
                                          filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    if filename:
        slider_frame = Frame(root)
        slider_frame.pack(pady=10, padx=10)

    
        faster_label = Label(slider_frame, text="Slower", font=("Arial", 10))
        faster_label.pack(side="left", padx=10)

        slower_label = Label(slider_frame, text="Faster", font=("Arial", 10))
        slower_label.pack(side="right", padx=5)  

    
        speed_slider = Scale(slider_frame, from_=2.0, to=0.1, resolution=0.01, orient=HORIZONTAL, label="Speed", length=300)
        speed_slider.set(0.5)  
        speed_slider.pack(padx=10)

        start_button = Button(root, text="Start", command=lambda: start_process(speed_slider.get()), width=20, height=2)
        start_button.pack(pady=20)  

Button(root, text="Choose File", command=choose_file, width=20, height=2).pack(pady=20)  

root.mainloop()
