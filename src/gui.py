from enum import Enum
import tkinter as tk
from tkinter import messagebox
import json

class languages(Enum):
    ENGLISCH = "english"
    DEUTSCH = "deutsch"

language = languages.DEUTSCH
source_path = ""
dic = json.load("./gui_dictionary.json")


def build_gui():
        
    def on_new_file():...

    def on_open_file():...

    def on_save_file():...

    def on_exit():
        root.quit()

    def on_undo():...

    def on_redo():...

    def on_about():...

    # Hauptfenster erstellen
    root = tk.Tk()
    root.title("Tkinter Menübeispiel")

    # Menüleiste erstellen
    menubar = tk.Menu(root)

    # "Datei"-Menü erstellen
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label=, command=on_new_file)
    file_menu.add_command(label="Öffnen", command=on_open_file)
    file_menu.add_command(label="Speichern", command=on_save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Beenden", command=on_exit)

    # "Bearbeiten"-Menü erstellen
    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Rückgängig", command=on_undo)
    edit_menu.add_command(label="Wiederholen", command=on_redo)

    # "Hilfe"-Menü erstellen
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="Dokumentation", command=on_about)
    help_menu.add_command(label="Über", command=on_about)

    # Menüs zur Menüleiste hinzufügen
    menubar.add_cascade(label="Datei", menu=file_menu)
    menubar.add_cascade(label="Bearbeiten", menu=edit_menu)
    menubar.add_cascade(label="Hilfe", menu=help_menu)


    # Menüleiste dem Hauptfenster zuweisen
    root.config(menu=menubar)

    # Hauptschleife starten
    root.mainloop()
