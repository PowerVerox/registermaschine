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

from constants import Constants

class DataManager:
    """Ein zentraler Datenmanager, der die gemeinsam genutzten Variablen verwaltet."""
    
    def __init__(self, root: tk.Tk):
        # Gemeinsame Variablen, die in der GUI und anderen Klassen verwendet werden
        self.registers: list[tk.StringVar] = [tk.StringVar(master=root, value="0") for _ in range(Constants.REGISTER_COUNT)]
        self.program_counter = tk.IntVar(master=root, value=1)