import pydirectinput
import time
import threading
import tkinter as tk
from tkinter import filedialog, Button, messagebox, Label, StringVar, Frame
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
    "Key10": "n", "Key11": "m", "Key12": ",", "Key13": "1", "Key14": ".",
    "Key15": "/"
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
        self.setup_ui()  # Setzt die Benutzeroberfläche auf
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Behandelt das Schließen des Fensters

    def setup_ui(self):
        """Initialisiert und konfiguriert die Benutzeroberfläche."""
        self.root.title("Music AutoPlayer for PC")  # Fenster-Titel
        self.root.geometry("450x300")  # Fenstergröße

        self.set_icon()  # Setzt das Anwendungs-Icon

        # Hinzufügen des Titel-Labels
        self.title_label = Label(self.root, text="Sky Auto Music Player", font=("Helvetica", 16, "bold"), pady=10)
        self.title_label.pack()

        # Rahmen für Schaltflächen
        self.button_frame = Frame(self.root, pady=10)
        self.button_frame.pack(fill=tk.X, padx=20)

        # Schaltfläche zum Auswählen einer Datei
        self.choose_file_button = Button(self.button_frame, text="Datei wählen", command=self.choose_file, font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", padx=15, pady=8)
        self.choose_file_button.pack(pady=5)

        # Status-Label zur Anzeige der ausgewählten Datei
        self.status_var = StringVar()
        self.status_label = Label(self.button_frame, textvariable=self.status_var, font=("Helvetica", 12))
        self.status_label.pack(pady=5)

        # Rahmen für Geschwindigkeits-Schaltflächen
        self.speed_frame = Frame(self.root)
        self.speed_frame.pack(fill=tk.X, padx=20)

    def set_icon(self):
        """Setzt das Icon für die Anwendung, wenn verfügbar."""        
        icon_path = "icon.ico"
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

    def choose_file(self):
        """Öffnet einen Dateidialog zur Auswahl einer Datei und zeigt die Geschwindigkeits-Schaltflächen an."""
        self.filename = filedialog.askopenfilename(
            title="Datei auswählen",
            initialdir="Songs",
            filetypes=(("Textdateien", "*.txt"), ("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*"))
        )
        if self.filename:
            self.status_var.set(f"Ausgewählte Datei:\n{os.path.basename(self.filename)}")
            self.show_speed_buttons()  # Zeigt die Schaltflächen zur Auswahl der Schreibgeschwindigkeit an

    def show_speed_buttons(self):
        """Zeigt Schaltflächen zur Auswahl der Schreibgeschwindigkeit an."""
        self.clear_frame(self.speed_frame)  # Löscht vorherige Schaltflächen
        button_frame = Frame(self.speed_frame)  # Neuer Rahmen für Schaltflächen
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Berechnung der Breite und des Abstands der Schaltflächen
        button_width = 8
        button_padx = 10

        for key, label in SPEEDS.items():
            Button(button_frame, text=label, command=lambda speed=key: self.start_process(speed), font=("Helvetica", 12), bg="#E0E0E0", fg="black", relief="flat", width=button_width, padx=15, pady=8).pack(side=tk.LEFT, padx=button_padx)

    def clear_frame(self, frame: Frame):
        """Löscht alle Widgets in einem gegebenen Frame."""
        for widget in frame.winfo_children():
            widget.destroy()

    def get_speed(self, speed_key: str) -> Optional[float]:
        """Gibt die Geschwindigkeit basierend auf dem übergebenen Schlüssel zurück."""
        speeds = {
            "slow": 0.5,
            "medium": 0.4,
            "fast": 0.3
        }
        return speeds.get(speed_key)

    def start_process(self, speed_key: str):
        """Startet den Prozess zum Simulieren von Tasteneingaben basierend auf der gewählten Geschwindigkeit."""
        if not self.filename:
            messagebox.showwarning("Keine Datei", "Bitte wählen Sie zuerst eine Datei aus.")
            return

        speed = self.get_speed(speed_key)
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
        except (ValueError, FileNotFoundError) as e:
            messagebox.showerror("Fehler", f"Fehler: {e}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Unbekannter Fehler: {e}")
        finally:
            self.root.deiconify()  # Zeigt das Fenster wieder an

    def read_file(self) -> str:
        """Liest den Inhalt der Datei basierend auf ihrem Typ (Text oder JSON)."""
        try:
            if self.filename.endswith(".json"):
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)
                if isinstance(data, list) and len(data) > 0 and "songNotes" in data[0]:
                    song_notes = data[0]["songNotes"]
                    return " ".join(self.get_note_key(note) for note in song_notes)
                raise ValueError("Die JSON-Datei hat das falsche Format oder enthält keine 'songNotes'.")
            with open(self.filename, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError("Die angegebene Datei wurde nicht gefunden.")
        except json.JSONDecodeError:
            raise ValueError("Die JSON-Datei konnte nicht decodiert werden.")

    def get_note_key(self, note: Dict) -> str:
        """Ersetzt den Key in der JSON-Datei durch das entsprechende Zeichen aus dem KEY_MAPPING."""
        return KEY_MAPPING.get(note["key"], "?")

    def replace_sent(self, sentence: str) -> str:
        """Ersetzt spezifische Platzhalter in einem Satz durch entsprechende Zeichen aus REPLACEMENTS."""
        for old, new in REPLACEMENTS.items():
            sentence = sentence.replace(old, new)
        return sentence

    def simulate_typing(self, sentence: str, speed: float):
        """Simuliert das Schreiben eines Satzes mit der angegebenen Geschwindigkeit."""
        def type_chars(chars: str):
            """Simuliert das Schreiben von Zeichen."""
            if chars:
                pydirectinput.write(chars)
            time.sleep(speed)  # Verzögerung anpassen

        group_chars = ''
        for char in sentence:
            if char == ' ':
                if group_chars:
                    threading.Thread(target=type_chars, args=(group_chars,)).start()
                    time.sleep(speed)  # Verzögerung zwischen Wörtern anpassen
                    group_chars = ''
                else:
                    time.sleep(speed * 0.5)  # Kurze Verzögerung bei aufeinander folgenden Leerzeichen
            else:
                group_chars += char
        if group_chars:
            threading.Thread(target=type_chars, args=(group_chars,)).start()

    def show_restart_message(self):
        """Zeigt eine Nachricht an, dass der Benutzer ein neues Lied auswählen kann."""
        messagebox.showinfo("Fertig", "Der Typvorgang ist abgeschlossen. Sie können ein neues Lied auswählen.")

    def on_closing(self):
        self.root.destroy()

# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicAutoPlayerApp(root)
    root.mainloop()
