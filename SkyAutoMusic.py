import pydirectinput
import time
import tkinter as tk
from tkinter import filedialog, Button, messagebox, Label, StringVar, Frame, Checkbutton, BooleanVar
import winsound
import os
import json
from typing import Optional, Dict

# Definiert die Geschwindigkeiten
SPEEDS = {
    "slow": "Langsam",
    "medium": "Mittel",
    "fast": "Schnell"
}

# Mapping der Noten-Keys zu Tastaturzeichen
KEY_MAPPING = {
    "Key0": "y", "Key1": "u", "Key2": "i", "Key3": "o", "Key4": "p",
    "Key5": "h", "Key6": "j", "Key7": "k", "Key8": "l", "Key9": ";",
    "Key10": "n", "Key11": "m", "Key12": ",", "Key13": ".", "Key14": "/"
}

# Ersetzt Platzhalter in der Eingabe durch entsprechende Zeichen
REPLACEMENTS = {
    "A1": "y", "A2": "u", "A3": "i", "A4": "o", "A5": "p",
    "B1": "h", "B2": "j", "B3": "k", "B4": "l", "B5": ";",
    "C1": "n", "C2": "m", "C3": ",", "C4": ".", "C5": "/"
}

class MusicAutoPlayerApp:
    def __init__(self, root: tk.Tk):
        """Initialisiert die Anwendung und richtet die Benutzeroberfläche ein."""
        self.root = root
        self.filename: Optional[str] = None
        self.long_press = BooleanVar()  # Variable für das lange Tastendrucken
        self.speed_selection = StringVar(value="")  # Variable zur Auswahl der Geschwindigkeit
        self.setup_ui()  # Setzt die Benutzeroberfläche auf
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Behandelt das Schließen des Fensters

    def setup_ui(self):
        """Initialisiert und konfiguriert die Benutzeroberfläche."""
        self.root.title("Music AutoPlayer for PC")  # Fenster-Titel
        self.root.geometry("400x350")  # Fenstergröße

        self.set_icon()  # Setzt das Anwendungs-Icon

        self.add_title()  # Fügt den Titel hinzu
        self.add_file_selection_button()  # Fügt die Dateiauswahl-Schaltfläche hinzu
        self.add_status_label()  # Fügt das Status-Label hinzu
        self.add_speed_buttons_frame()  # Fügt den Rahmen für die Geschwindigkeits-Schaltflächen hinzu
        self.add_checkbox_and_play_button()  # Fügt die Checkbox und den Play-Button hinzu

    def set_icon(self):
        """Setzt das Icon für die Anwendung, wenn verfügbar.""" 
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

    def add_title(self):
        """Fügt den Titel zur Oberfläche hinzu.""" 
        self.title_label = Label(self.root, text="Sky Auto Music Player", font=("Helvetica", 16, "bold"), pady=10)
        self.title_label.pack()

    def add_file_selection_button(self):
        """Fügt die Schaltfläche zum Auswählen einer Datei hinzu.""" 
        self.button_frame = Frame(self.root, pady=10)
        self.button_frame.pack(fill=tk.X, padx=20)
        self.choose_file_button = Button(self.button_frame, text="Datei wählen", command=self.choose_file,
                                         font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", padx=15,
                                         pady=8)
        self.choose_file_button.pack(pady=5)

    def add_status_label(self):
        """Fügt das Label für den Dateistatus hinzu.""" 
        self.status_var = StringVar()
        self.status_label = Label(self.button_frame, textvariable=self.status_var, font=("Helvetica", 12))
        self.status_label.pack(pady=5)

    def add_speed_buttons_frame(self):
        """Fügt den Rahmen für die Geschwindigkeits-Schaltflächen hinzu.""" 
        self.speed_frame = Frame(self.root)
        self.speed_frame.pack(fill=tk.X, padx=20)

    def add_checkbox_and_play_button(self):
        """Fügt die Checkbox und den Play-Button hinzu.""" 
        self.long_press_checkbox = Checkbutton(self.root, text="Lange Tasten drücken", variable=self.long_press, font=("Helvetica", 12))
        self.play_button = Button(self.root, text="Starten", command=self.start_process, state=tk.DISABLED, font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", padx=15, pady=8)

    def choose_file(self):
        """Öffnet einen Dateidialog zur Auswahl einer Datei und zeigt die Geschwindigkeits-Schaltflächen an.""" 
        self.filename = filedialog.askopenfilename(
            title="Datei auswählen",
            initialdir="Songs",
            filetypes=(("Textdateien", "*.txt"), ("JSON-Dateien", "*.json"))
        )
        if self.filename:
            self.status_var.set(f"Ausgewählte Datei:\n{os.path.basename(self.filename)}")
            self.show_speed_buttons()
            self.long_press_checkbox.pack(pady=5)
            self.play_button.pack(pady=10)

    def show_speed_buttons(self):
        """Zeigt Schaltflächen zur Auswahl der Schreibgeschwindigkeit an.""" 
        self.clear_frame(self.speed_frame)
        button_frame = Frame(self.speed_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        for key, label in SPEEDS.items():
            Button(button_frame, text=label, command=lambda speed=key: self.select_speed(speed),
                   font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", padx=15, pady=8).pack(side=tk.LEFT, padx=10)

    def select_speed(self, speed_key: str):
        """Speichert die ausgewählte Geschwindigkeit und aktiviert den Play-Button.""" 
        self.speed_selection.set(speed_key)
        self.play_button.config(state=tk.NORMAL)

    def clear_frame(self, frame: Frame):
        """Entfernt alle Widgets aus einem Frame.""" 
        for widget in frame.winfo_children():
            widget.destroy()

    def get_speed(self) -> Optional[float]:
        """Gibt die Geschwindigkeit basierend auf der Auswahl zurück.""" 
        speeds = {"slow": 0.03, "medium": 0.02, "fast": 0.01}
        return speeds.get(self.speed_selection.get())

    def start_process(self):
        """Startet den Prozess zum Simulieren von Tasteneingaben basierend auf der gewählten Geschwindigkeit."""
        if not self.filename:
            messagebox.showwarning("Keine Datei", "Bitte wählen Sie zuerst eine Datei aus.")
            return

        speed = self.get_speed()
        if speed is None:
            messagebox.showwarning("Ungültige Geschwindigkeit", "Die angegebene Geschwindigkeit ist ungültig.")
            return

        self.root.withdraw()  # Versteckt das Hauptfenster
        try:
            original_sentence = self.read_file()  # Liest den Inhalt der Datei
            modified_sentence = self.replace_sent(original_sentence)  # Ersetzt Platzhalter durch Zeichen
            time.sleep(1)  # Kurze Verzögerung vor dem Start der Typ-Simulation
            self.simulate_typing(modified_sentence, speed)  # Simuliert das Schreiben
            winsound.Beep(1000, 500)  # Beispielton bei Beendigung
            self.show_restart_message()  # Zeigt eine Nachricht an, dass der Benutzer ein neues Lied auswählen kann
        except Exception as e:
            messagebox.showerror("Fehler", f"Unbekannter Fehler: {e}")
        finally:
            self.root.deiconify()

    def read_file(self) -> str:
        """Liest den Inhalt der Datei basierend auf ihrem Typ (Text oder JSON)."""
        if self.filename.endswith(".json"):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            song_notes = data[0].get("songNotes", [])
            return " ".join(self.get_note_key(note) for note in song_notes)
        else:
            with open(self.filename, "r", encoding="utf-8") as file:
                return file.read().strip()

    def get_note_key(self, note: Dict) -> str:
        """Ersetzt den Key in der JSON-Datei durch das entsprechende Zeichen aus dem KEY_MAPPING."""
        return KEY_MAPPING.get(note["key"], "?")

    def parse_json(self, json_content: str) -> str:
        """Parst JSON-Inhalt und gibt den Text zurück.""" 
        data = json.loads(json_content)
        return data.get('text', '')

    def replace_sent(self, content: str) -> str:
        """Ersetzt Platzhalter durch entsprechende Zeichen.""" 
        for placeholder, replacement in REPLACEMENTS.items():
            content = content.replace(placeholder, replacement)
        return content

    def simulate_typing(self, sentence: str, speed: float):
        """Simuliert das Schreiben eines Satzes mit der angegebenen Geschwindigkeit, 
        unter Berücksichtigung von normalen oder langen Tastenanschlägen je nach Checkbox.""" 
    
        def type_short_press(char: str):
            """Simuliert das Schreiben eines einzelnen Zeichens mit normaler Geschwindigkeit.""" 
            pydirectinput.write(char)
            time.sleep(speed)

        def type_long_press(char: str):
            """Simuliert das Schreiben eines einzelnen Zeichens mit langem Tastendruck.""" 
            pydirectinput.keyDown(char)
            time.sleep(0.2)  # Dauer des langen Tastendrucks
            pydirectinput.keyUp(char)

        long_press_active = self.long_press.get()

        for char in sentence:
            if char == ' ':  # Leerzeichen erkannt
                # Zeit für das Leerzeichen - aktuell auskommentiert
                time.sleep(speed * 0.5)
                #time.sleep(speed)
                pass
            else:
                if long_press_active:
                    type_long_press(char)
                else:
                    type_short_press(char)

    def show_restart_message(self):
        """Zeigt eine Nachricht an, dass der Benutzer ein neues Lied auswählen kann.""" 
        messagebox.showinfo("Fertig", "Song beendet. Möchten Sie ein neues Lied auswählen?")

    def on_closing(self):
        """Behandelt das Schließen des Fensters.""" 
        self.root.destroy()

# Main App
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicAutoPlayerApp(root)
    root.mainloop()
