import pydirectinput
import time
import threading
import tkinter as tk
from tkinter import filedialog, Button, messagebox, Label, StringVar, Frame
import winsound
import os
import json
from typing import Optional, Dict

# Defines the speeds
SPEEDS = {
    "slow": "Slow",
    "medium": "Medium",
    "fast": "Fast"
}

# Mapping of note keys to keyboard characters
KEY_MAPPING = {
    "Key0": "y", "Key1": "u", "Key2": "i", "Key3": "o", "Key4": "p",
    "Key5": "h", "Key6": "j", "Key7": "k", "Key8": "l", "Key9": ";",
    "Key10": "n", "Key11": "m", "Key12": ",", "Key13": "1", "Key14": ".",
    "Key15": "/"
}

# Replaces placeholders in the input with corresponding characters
REPLACEMENTS = {
    "A1": "y", "A2": "u", "A3": "i", "A4": "o", "A5": "p",
    "B1": "h", "B2": "j", "B3": "k", "B4": "l", "B5": ";",
    "C1": "n", "C2": "m", "C3": ",", "C4": ".", "C5": "/"
}

class MusicAutoPlayerApp:
    def __init__(self, root: tk.Tk):
        """Initializes the application and sets up the user interface."""
        self.root = root
        self.filename: Optional[str] = None
        self.setup_ui()  # Sets up the user interface
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handles window close event

    def setup_ui(self):
        """Initializes and configures the user interface."""
        self.root.title("Music AutoPlayer for PC")  # Window title
        self.root.geometry("450x300")  # Window size

        self.set_icon()  # Sets the application icon

        # Adding the title label
        self.title_label = Label(self.root, text="Sky Auto Music Player", font=("Helvetica", 16, "bold"), pady=10)
        self.title_label.pack()

        # Frame for buttons
        self.button_frame = Frame(self.root, pady=10)
        self.button_frame.pack(fill=tk.X, padx=20)

        # Button to choose a file
        self.choose_file_button = Button(self.button_frame, text="Choose File", command=self.choose_file, font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", padx=15, pady=8)
        self.choose_file_button.pack(pady=5)

        # Status label to display the selected file
        self.status_var = StringVar()
        self.status_label = Label(self.button_frame, textvariable=self.status_var, font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        # Frame for speed buttons
        self.speed_frame = Frame(self.root)
        self.speed_frame.pack(fill=tk.X, padx=20)

    def set_icon(self):
        """Sets the icon for the application, if available."""        
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

    def choose_file(self):
        """Opens a file dialog to select a file and shows speed buttons."""    
        self.filename = filedialog.askopenfilename(
            title="Select File",
            initialdir="Songs",
            filetypes=(("Text Files", "*.txt"), ("JSON Files", "*.json"), ("All Files", "*.*"))
        )
        if self.filename:
            self.status_var.set(f"Selected File:\n{os.path.basename(self.filename)}")
            self.show_speed_buttons()  # Shows buttons for speed selection

    def show_speed_buttons(self):
        """Shows buttons for selecting playback speed."""
        self.clear_frame(self.speed_frame)  # Clears previous buttons
        button_frame = Frame(self.speed_frame)  # New frame for buttons
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Calculates button width and padding
        button_width = 8
        button_padx = 10

        for key, label in SPEEDS.items():
            Button(button_frame, text=label, command=lambda speed=key: self.start_process(speed), font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", width=button_width, padx=15, pady=8).pack(side=tk.LEFT, padx=button_padx)

    def clear_frame(self, frame: Frame):
        """Clears all widgets in a given frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def get_speed(self, speed_key: str) -> Optional[float]:
        """Returns the speed based on the provided key."""
        speeds = {
            "slow": 0.5,
            "medium": 0.4,
            "fast": 0.3
        }
        return speeds.get(speed_key)

    def start_process(self, speed_key: str):
        """Starts the process of simulating keystrokes based on the chosen speed."""
        if not self.filename:
            messagebox.showwarning("No File", "Please select a file first.")
            return

        speed = self.get_speed(speed_key)
        if speed is None:
            messagebox.showwarning("Invalid Speed", "The specified speed is invalid.")
            return

        self.root.withdraw()  # Hides the main window
        try:
            original_sentence = self.read_file()  # Reads the file content
            modified_sentence = self.replace_sent(original_sentence)  # Replaces placeholders with characters
            time.sleep(1)  # Short delay before starting typing simulation
            self.simulate_typing(modified_sentence, speed)  # Simulates typing
            winsound.Beep(1000, 500)  # Example sound on completion
            self.show_restart_message()  # Shows a message indicating that the user can select a new song
        except (ValueError, FileNotFoundError) as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unknown Error: {e}")
        finally:
            self.root.deiconify()  # Shows the window again

    def read_file(self) -> str:
        """Reads the content of the file based on its type (text or JSON)."""
        try:
            if self.filename.endswith(".json"):
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                if isinstance(data, list) and len(data) > 0 and "songNotes" in data[0]:
                    song_notes = data[0]["songNotes"]
                    return " ".join(self.get_note_key(note) for note in song_notes)
                raise ValueError("The JSON file has the wrong format or does not contain 'songNotes'.")
            with open(self.filename, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError("The specified file was not found.")
        except json.JSONDecodeError:
            raise ValueError("The JSON file could not be decoded.")

    def get_note_key(self, note: Dict) -> str:
        """Replaces the key in the JSON file with the corresponding character from KEY_MAPPING."""
        return KEY_MAPPING.get(note["key"], "?")

    def replace_sent(self, sentence: str) -> str:
        """Replaces specific placeholders in a sentence with corresponding characters from REPLACEMENTS."""
        for old, new in REPLACEMENTS.items():
            sentence = sentence.replace(old, new)
        return sentence

    def simulate_typing(self, sentence: str, speed: float):
        """Simulates typing a sentence with the given speed."""
        def type_chars(chars: str):
            """Simulates typing characters."""
            if chars:
                pydirectinput.write(chars)
            time.sleep(speed)  # Adjust delay

        group_chars = ''
        for char in sentence:
            if char == ' ':
                if group_chars:
                    threading.Thread(target=type_chars, args=(group_chars,)).start()
                    time.sleep(speed)  # Adjust delay between words
                    group_chars = ''
                else:
                    time.sleep(speed * 0.5)  # Short delay for consecutive spaces
            else:
                group_chars += char
        if group_chars:
            threading.Thread(target=type_chars, args=(group_chars,)).start()

    def show_restart_message(self):
        """Shows a message indicating that the user can select a new song."""
        messagebox.showinfo("Done", "The typing process is complete. You can select a new song.")

    def on_closing(self):
        self.root.destroy()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicAutoPlayerApp(root)
    root.mainloop()
