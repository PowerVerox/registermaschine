import tkinter as tk

from constants import Constants

class DataManager:
    """Ein zentraler Datenmanager, der die gemeinsam genutzten Variablen verwaltet."""
    
    def __init__(self, root: tk.Tk):
        # Gemeinsame Variablen, die in der GUI und anderen Klassen verwendet werden
        self.registers: list[tk.StringVar] = [tk.StringVar(master=root, value="0") for _ in range(Constants.REGISTER_COUNT)]
        self.program_counter = tk.IntVar(master=root, value=1)