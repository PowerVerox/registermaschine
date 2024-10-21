# registermaschine - A simple register machine simulator
# Copyright (C) 2024  Tim Ernst, Vincent A. Hey

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import tkinter as tk
from tkinter import filedialog

from constants import *
from machine import *

class Gui:
    def __init__(self, root: tk.Tk, data_manager: DataManager, machine: Machine):
        self.root = root
        self.datamanager = data_manager
        self.machine = machine

        self.editable = True # Flag für die Bearbeitbarkeit des Textfelds
        self.current_file_path = None
        self.auto_increment_active = False  # Flag für die automatische Inkrementierung (play aktiv)

        # Erstellen der GUI-Komponenten
        self.root.geometry("800x600")  # Größe des Fensters festlegen
        self.root.resizable(False, False) # Fenstergröße nicht veränderbar
        self.root.title("Registermaschine")

        self.build_main_frame()
        self.build_left_panel()
        self.build_text_area()
        self.build_menu()
        self.build_status_bar()

        # Event-Handler für das Textfeld
        self.text_area.bind('<KeyRelease>', self.update_line_numbers)
        self.text_area.bind('<MouseWheel>', self.update_line_numbers)
        self.text_area.bind('<ButtonRelease-1>', self.update_line_numbers)

        # Zeilennummern beim Start richtig anzeigen
        self.update_line_numbers()

    def build_main_frame(self):
        """Erstellt den Hauptframe, der den linken und rechten Bereich umfasst."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')

    def build_left_panel(self):
        """Erstellt den linken Bereich mit Constants.REGISTER_COUNT Zahleneingabefeldern, 
        Binäranzeigen Steuerungsschaltflächen und Program Counter."""
        self.left_frame = tk.Frame(self.main_frame, width=200, bg='lightgrey')
        self.left_frame.pack(side='left', fill='both', padx=10, pady=10)

        # Erstellen von Constants.REGISTER_COUNT Zahleneingabefeldern und Binäranzeigen
        self.leds_list = []

        for i, integer_var in enumerate(self.datamanager.registers):
            # Label und Eingabefeld für die Register
            integer_label = tk.Label(self.left_frame, text="     Akku    " if i == 0 else f"Register {i}:")
            integer_label.grid(row=i, column=0, pady=5, padx=5, sticky='e')

            # StringVar für das Eingabefeld, damit Änderungen überwacht werden können
            integer_var.trace_add("write", lambda name, index, mode, var=integer_var, idx=i: self.update_binary_representation(var, idx))

            # Eingabefeld für den Registerwert
            vcmd = (self.left_frame.register(self.validate_integer), '%P')
            integer_entry = tk.Entry(self.left_frame, textvariable=integer_var, validate='key', validatecommand=vcmd, width=10)
            integer_entry.grid(row=i, column=1, pady=5, padx=5)

            # Frame für die LEDs (Binärdarstellung) rechts neben dem Eingabefeld
            binary_frame = tk.Frame(self.left_frame)
            binary_frame.grid(row=i, column=2, pady=5, padx=5)

            leds = [tk.Label(binary_frame, text='0', width=2, bg='white', relief='ridge') for _ in range(Constants.REGISTER_LIMIT.bit_length()-1)]
            for led in leds:
                led.pack(side='left', padx=1)

            # Speichern von Eingabefeld und LEDs zur späteren Verwendung
            self.leds_list.append(leds)

        # Program Counter Label
        program_counter_label = tk.Label(self.left_frame, text="Program Counter:")
        program_counter_label.grid(row=Constants.REGISTER_COUNT, column=0, pady=10, padx=5, sticky='e')

        # Anzeige des Werts des Program Counters
        self.pc_display = tk.Label(self.left_frame, textvariable=self.datamanager.program_counter, relief='sunken', width=10)
        self.pc_display.grid(row=Constants.REGISTER_COUNT, column=1, pady=10, padx=5)

        # Reset-Button
        self.step_button = tk.Button(self.left_frame, text="Reset", command=self.reset)
        self.step_button.grid(row=Constants.REGISTER_COUNT+1, column=0, pady=10, padx=5)

        # Step-Button
        self.step_button = tk.Button(self.left_frame, text="Step", command=self.step)
        self.step_button.grid(row=Constants.REGISTER_COUNT+1, column=1, pady=10, padx=5)

        # Play/Pause-Button
        self.play_button = tk.Button(self.left_frame, text="Play", command=self.toggle_play_pause)
        self.play_button.grid(row=Constants.REGISTER_COUNT+1, column=2, pady=10, padx=5)

        # Textfeld für die Anzeige von Exceptions
        self.exception_frame = tk.Frame(self.left_frame)
        self.exception_frame.grid(row=Constants.REGISTER_COUNT+2, column=0, columnspan=3, pady=10, padx=5)
        self.exception_text = tk.Text(self.exception_frame, height=8, width=50, wrap='word', fg='red')
        self.exception_text.configure(state='disabled')
        self.exception_text.pack(expand=True, fill='both')

    def show_exception(self, message):
        """Zeigt eine Ausnahmemeldung an."""
        self.exception_text.configure(state='normal')
        self.exception_text.insert(tk.END, message + '\n')
        self.exception_text.configure(state='disabled')
        self.exception_text.see(tk.END)

    def build_text_area(self):
        """Erstellt den Textbereich mit Scrollbar und Zeilennummern."""
        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack(side='right', expand=True, fill='both')

        # Canvas für die Zeilennummern
        self.line_numbers = tk.Canvas(self.text_frame, width=40, bg='lightgrey')
        self.line_numbers.pack(side='left', fill='y')

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side='right', fill='y')

        # Textbereich
        self.text_area = tk.Text(self.text_frame, wrap='word', yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill='both')

        self.scrollbar.config(command=self.scrollbar_command)

    def scrollbar_command(self, *args):
        """Verknüpft die Scrollbar mit dem Textbereich. Zeilennummern werden aktualisiert."""
        self.text_area.yview(*args)
        self.update_line_numbers()
        

    def build_menu(self):
        """Erstellt die Menüleiste mit den Menüs 'Datei' und 'Bearbeiten'."""
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menü "Datei"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Datei", menu=self.file_menu)
        self.file_menu.add_command(label="Öffnen", command=self.open_file)
        self.file_menu.add_command(label="Speichern", command=self.save_file)
        self.file_menu.add_command(label="Speichern unter", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Beenden", command=self.root.quit)

        # Menü "Bearbeiten"
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Bearbeiten", menu=self.edit_menu)
        self.edit_menu.add_command(label="Bearbeiten umschalten", command=self.toggle_editable)
        self.highlight_program_counter_line()

    def build_status_bar(self):
        """Erstellt die Statusleiste am unteren Rand des Fensters."""
        self.status_bar = tk.Label(self.root, text="Bearbeiten: Ein", bd=1, relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

    def open_file(self):
        """Öffnet eine Datei und lädt ihren Inhalt in das Textfeld."""
        file_path = filedialog.askopenfilename(defaultextension=".ram",
                                               filetypes=[("RAM Dateien", "*.ram"), ("Alle Dateien", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file_path = file_path
                self.status_bar.config(text=f"Geöffnet: {file_path}")
                self.update_line_numbers()  
            except Exception as e:
                self.show_exception(f"Datei konnte nicht geöffnet werden: {e}")

    def save_file(self):
        """Speichert den Inhalt des Textfelds in die zuletzt 
        geöffnete Datei oder "speichern unter"-Dialog."""
        if self.current_file_path:
            try:
                with open(self.current_file_path, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                self.status_bar.config(text=f"Gespeichert: {self.current_file_path}")
            except Exception as e:
                self.show_exception(f"Datei konnte nicht gespeichert werden: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Speichert den Inhalt des Textfelds in einer Datei, die durch einen Dateidialog ausgewählt wird."""
        file_path = filedialog.asksaveasfilename(defaultextension=".ram",
                                                 filetypes=[("RAM Dateien", "*.ram"), ("Alle Dateien", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                self.current_file_path = file_path
                self.status_bar.config(text=f"Gespeichert unter: {file_path}")
            except Exception as e:
                self.show_exception(f"Datei konnte nicht gespeichert werden: {e}")

    def toggle_editable(self):
        """Schaltet das Textfeld zwischen Bearbeitungs- und Anzeige-/Ausführungsmodus um.
        Lädt das Programm in die Maschine, wenn der Bearbeitungsmodus verlassen wird."""
        if not self.auto_increment_active:
            self.editable = not self.editable
            self.text_area.config(state=tk.NORMAL if self.editable else tk.DISABLED)
            self.status_bar.config(text=f"Bearbeiten: {'Ein' if self.editable else 'Aus'}")
            if not self.editable:
                try:
                    self.machine.program = Program.from_string(self.text_area.get(1.0, tk.END))
                except Exception as e:
                    self.show_exception(f"Programm konnte nicht geladen werden: {e}")

    def validate_integer(self, value_if_allowed):
        """Validiert das Eingabefeld auf ganzzahlige positive Werte oder leer."""
        return value_if_allowed.isdigit() or value_if_allowed == ""

    def update_binary_representation(self, var, idx):
        """Aktualisiert die binäre Repräsentation basierend auf dem Eingabefeld."""
        try:
            value = 0 if var.get() == "" else int(var.get()) # Wenn das Feld leer ist, setze den Wert auf 0, 
                                                             # sonst konvertiere den Wert in eine Ganzzahl 
                                                             # nötig, da sonst ValueError bei leerem String ("")

            if value > 255:
                # Kleiner als 0 unmoeglich, da keine Sonderzeichen eingegeben werden koennen, wenn im Programm Minuszahl --> Modulare Arithmetik
                raise ValueError("Die Zahl muss zwischen 0 und 255 liegen.")

            binary_rep = format(value, '08b')
            for i, bit in enumerate(binary_rep):
                self.leds_list[idx][i].config(text=bit, bg='red' if bit == '1' else 'white')
        except ValueError:
            var.set("255")
            # Wenn der Wert ungültig ist (zu groß), setze alle LEDs auf 1 --> 255 (höchster Wert)
            for led in self.leds_list[idx]:
                led.config(text='1', bg='red')
            self.show_exception("Ungültige Eingabe: Bitte eine Zahl zwischen 0 und 255 eingeben.")

    def reset(self):
        """Setzt den Program Counter auf 1 und setzt alle Register auf 0."""
        self.machine.clear_memory()
        self.datamanager.program_counter.set(1)
        self.highlight_program_counter_line()
        self.exception_text.configure(state='normal')
        self.exception_text.delete(1.0, tk.END)
        self.exception_text.configure(state='disabled')

    def step(self):
        """Inkrementiert den Program Counter um 1 und aktualisiert die Zeilenhervorhebung."""
        if not self.editable:
            try:
                self.machine.step()
            except Exception as e:
                self.show_exception(str(e))
            self.highlight_program_counter_line()

    def toggle_play_pause(self):
        """Wechselt zwischen automatischer Inkrementierung (play) und Pause."""
        if self.auto_increment_active:
            # Pausiere die automatische Inkrementierung
            self.auto_increment_active = False
            self.play_button.config(text="Play")
        elif not self.editable:
            # Starte die automatische Inkrementierung
            self.auto_increment_active = True
            self.play_button.config(text="Pause")
            self.auto_increment()

    def auto_increment(self):
        """Erhöht den Program Counter automatisch in Intervallen (1 Sek.), bis der Play-Button wieder gedrückt wird."""
        if self.auto_increment_active:
            self.step()
            self.highlight_program_counter_line()
            self.root.after(1000, self.auto_increment)  # Wird wieder aufgerufen, nach 1 Sekunde

    def highlight_program_counter_line(self):
        """Markiert die Zeile, auf die der Program Counter zeigt."""
        # Entferne vorherige Hervorhebung
        self.text_area.tag_remove('highlight', '1.0', tk.END)
        
        # Hole die Zeile, die hervorgehoben werden soll
        line_num = self.datamanager.program_counter.get()
        self.text_area.tag_add('highlight', f'{line_num}.0', f'{line_num}.0 lineend')
        self.text_area.tag_configure('highlight', background='yellow')

    def update_line_numbers(self, event=None):
        """Aktualisiert die Zeilennummern des Texteditors."""
        self.line_numbers.delete("all")

        i = self.text_area.index("@0,0")
        while True:
            dline = self.text_area.dlineinfo(i) 
            if dline is None:
                break
            y = dline[1]
            line_number = str(i).split(".")[0]
            self.line_numbers.create_text(2, y, anchor="nw", text=line_number, fill="black")
            i = self.text_area.index(f"{i}+1line")
        self.highlight_program_counter_line()
