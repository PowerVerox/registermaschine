import tkinter as tk

from constants import Constants

class DataManager:
    """Ein zentraler Datenmanager, der die gemeinsam genutzten Variablen verwaltet."""
    
    def __init__(self, root: tk.Tk):
        # Gemeinsame Variablen, die in der GUI und anderen Klassen verwendet werden
        self.entries: list[tk.StringVar] = [tk.StringVar(master=root, value="0") for _ in range(Constants.REGISTER_COUNT)]
        self.program_counter = tk.IntVar(master=root, value=1)
    

    def set_program_counter(self, value):
        """Setzt den Wert des Program Counters."""
        self.program_counter.set(value)

    def get_program_counter(self):
        """Gibt den Wert des Program Counters zurück."""
        return self.program_counter.get()
    