
import tkinter as tk
from tkinter import filedialog, messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Texteditor")
        
        # Hauptframe für linke und rechte Seite
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')

        # Linker Bereich für zusätzliche Anzeigen
        self.left_frame = tk.Frame(self.main_frame, width=200, bg='lightgrey')
        self.left_frame.pack(side='left', fill='both')

        # Eingabefeld für ganze Zahl
        self.integer_label = tk.Label(self.left_frame, text="Ganze Zahl:")
        self.integer_label.pack(pady=5)

        # Validation Command für Eingabefeld
        vcmd = (self.left_frame.register(self.validate_integer), '%P')
        self.integer_entry = tk.Entry(self.left_frame, validate='key', validatecommand=vcmd)
        self.integer_entry.pack(pady=5)
        self.integer_entry.bind("<KeyRelease>", self.update_binary_representation)

        # Anzeige der Binärdarstellung
        self.binary_label = tk.Label(self.left_frame, text="Binärdarstellung:")
        self.binary_label.pack(pady=5)
        self.binary_frame = tk.Frame(self.left_frame)
        self.binary_frame.pack(pady=5)

        # 8 LEDs (Label) für die Binärdarstellung
        self.leds = [tk.Label(self.binary_frame, text='0', width=2, bg='white', relief='ridge') for _ in range(8)]
        for led in self.leds:
            led.pack(side='left', padx=2)

        # Textbereich für den Editor auf der rechten Seite mit Scrollbar
        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack(side='right', expand=True, fill='both')

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side='right', fill='y')

        self.text_area = tk.Text(self.text_frame, wrap='word', yscrollcommand=self.scrollbar.set)
        self.text_area.pack(expand=True, fill='both')

        self.scrollbar.config(command=self.text_area.yview)

        # Menüleiste erstellen
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

        # Statusleiste
        self.status_bar = tk.Label(self.root, text="Bearbeiten: Ein", bd=1, relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

        self.editable = True
        self.current_file_path = None

    def open_file(self):
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
            except Exception as e:
                messagebox.showerror("Fehler", f"Datei konnte nicht geöffnet werden: {e}")

    def save_file(self):
        if self.current_file_path:
            try:
                with open(self.current_file_path, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                self.status_bar.config(text=f"Gespeichert: {self.current_file_path}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Datei konnte nicht gespeichert werden: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
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
                messagebox.showerror("Fehler", f"Datei konnte nicht gespeichert werden: {e}")

    def toggle_editable(self):
        self.editable = not self.editable
        state = 'normal' if self.editable else 'disabled'
        self.text_area.config(state=state)
        self.status_bar.config(text=f"Bearbeiten: {'Ein' if self.editable else 'Aus'}")

    def validate_integer(self, P):
        """ Validiert, dass die Eingabe nur ganze positive Zahlen enthält. """
        if P.isdigit() or P == "":
            return True
        return False

    def update_binary_representation(self, event=None):
        # Holen Sie sich den Wert aus dem Eingabefeld
        value = self.integer_entry.get()
        if value.isdigit():
            number = int(value)
            if 0 <= number <= 255:
                # Berechnen Sie die Binärdarstellung
                binary_representation = format(number, '08b')
                # Aktualisieren Sie die LEDs
                for i, bit in enumerate(binary_representation):
                    self.leds[i].config(text=bit, bg='red' if bit == '1' else 'white')
            else:
                messagebox.showwarning("Warnung", "Bitte geben Sie eine Zahl zwischen 0 und 255 ein.")
        else:
            for led in self.leds:
                led.config(text='0', bg='white')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Größe des Fensters festlegen
    editor = TextEditor(root)
    root.mainloop()
