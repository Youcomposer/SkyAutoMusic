import pydirectinput
import time
import threading
import os
from tkinter import Tk, filedialog, Button

# Define the speeds
SPEED_SLOW = 0.4
SPEED_MEDIUM = 0.5
SPEED_FAST = 0.6

def replaceSent(sentence):
    return sentence.replace("A1", "y").replace("A2", "u").replace("A3", "i").replace("A4", "o").replace("A5", "p").replace("B1", "h").replace("B2", "j").replace("B3", "k").replace("B4", "l").replace("B5", ";").replace("C1", "n").replace("C2", "m").replace("C3", ",").replace(".", "1").replace("C4", ".").replace("C5", "/")

def press_keys(keys):
    for key in keys:
        pydirectinput.keyDown(key)
    time.sleep(0.1)
    for key in keys:
        pydirectinput.keyUp(key)

def start_process(speed):
    global filename
    global root
    root.destroy()  # Close the popup window

    # Read the original from the file
    with open(filename, "r") as file:
        original_sentence = file.read().strip()

    # Modify the original sentence
    modified_sentence = replaceSent(original_sentence)

    # Simulate typing the modified sentence
    time.sleep(1)
    group_chars = ''
    for char in modified_sentence:
        if char == ' ':
            if group_chars:
                threading.Thread(target=press_keys, args=(group_chars,)).start()
                time.sleep(speed)  # Adjust the sleep time here
                group_chars = ''
            else:
                time.sleep(0.3)
        else:
            group_chars += char
    if group_chars:
        threading.Thread(target=press_keys, args=(group_chars,)).start()

# Initialize tkinter
root = Tk()
root.title("Music AutoPlayer PC")
root.geometry("300x150")

# Set custom icon using relative path
current_dir = os.path.dirname(os.path.realpath(__file__))
icon_path = os.path.join(current_dir, "icon.ico")
root.iconbitmap(icon_path)

def choose_file():
    global filename
    initial_dir = os.path.join(current_dir, "Songs")  # Set initial directory to current directory + Songs
    filename = filedialog.askopenfilename(title="Select a file", initialdir=initial_dir, filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    if filename:
        slow_button.pack()
        medium_button.pack()
        fast_button.pack()

# Create buttons for choosing speed
def choose_speed(speed):
    return lambda: start_process(speed)

slow_button = Button(root, text="Slow", command=choose_speed(SPEED_SLOW))
medium_button = Button(root, text="Medium", command=choose_speed(SPEED_MEDIUM))
fast_button = Button(root, text="Fast", command=choose_speed(SPEED_FAST))

# Create a button to choose a file
choose_file_button = Button(root, text="Choose File", command=choose_file)
choose_file_button.pack()

root.mainloop()
