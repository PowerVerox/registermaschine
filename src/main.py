from gui import *

def main():
    root = tk.Tk()
    datamanager = DataManager(root)
    machine = Machine(datamanager).add_standard_instructions()
    gui = Gui(root, datamanager, machine)
    gui.root.mainloop()

if __name__ == "__main__":
    main()
