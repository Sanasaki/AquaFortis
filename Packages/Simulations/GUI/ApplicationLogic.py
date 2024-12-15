import tkinter as tk
from tkinter import ttk


class SimulationGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lammps Job Builder")
        self.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._setupButtons()
        self._setupTreeview()

    def _setupButtons(self):
        self.buttonFrame = tk.Frame(self)
        self.addSimulationButton = tk.Button(self.buttonFrame, text="ButtonText", command=self.callBack)
        self.exitButton = tk.Button(self.buttonFrame, text="Exit", command=self.quit)
        self.addSimulationButton.pack(side="left")
        self.exitButton.pack(side="right")
        self.buttonFrame.pack(side="bottom")

    def _setupTreeview(self):
        self.treeFrame = tk.Frame(self)
        self.tree = ttk.Treeview(self.treeFrame)
        self.tree["columns"] = ("Col1", "Col2")
        self.tree.heading("#0", text="First level")
        self.tree.heading("Col1", text="Attr 1")
        self.tree.heading("Col2", text="Attr 2")
        self.tree.pack(fill="both", expand=True)
        self.treeFrame.pack(side="top", fill="both", expand=True)

    def callBack(self):
        print("PlaceHolder function")
        pass


def main():
    app = SimulationGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
