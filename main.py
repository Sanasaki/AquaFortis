import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox, ttk

import config
from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule
from Classes.FileTypes.File import File
from Classes.FileTypes.FileXYZ import FileXYZ
from Classes.Speciation import Speciation
from Classes.Trajectory import FileTrajectory


def writeFile(exportPath: str, speciations, name):
    path = exportPath + f'/{name}-speciation.txt'
    print("Writing:", name)
    with open(path, 'a') as outfile:
        for i, item in enumerate(speciations):
            outfile.write(f"{i} {item}\n")


def main(**argv):
    def printSelection():
        try:
            item = treeview.selection()[0]
        except IndexError:
            messagebox.showwarning("Warning", "Please select a frame")
        else:
            text = treeview.item(item, option="text")
            messagebox.showinfo("Frame", f"Frame {text}")
            
    
    # someSpeciation = Speciation.fromStr("4 {HNO3: 16, H2O: 76, H3NO4: 4}")

    # nitrogen = Atom("N")
    # hydrogen = Atom("H")
    # oxygen = Atom("O")
    # listAtoms = [hydrogen, nitrogen, oxygen, oxygen, oxygen]
    
    
    # someMol = Molecule("HNO3")
    # print(someMol)

    # someOtherMol = Molecule(listAtoms)
    # print(someOtherMol)
    selectedXyzFiles = fd.askopenfilenames(title='Select XYZ files', initialdir=r'C:\Users\JL252842\Documents\Thesis\Data\Raw\Simulations\2024-11-22\AIMD-SCAN-AF')

    # print(someSpeciation.getFrame(2000))
    root = tk.Tk()
    root.title("Explore speciation")
    root.geometry("800x600")
    ttk.Style().configure("TButton", padding=6, relief="flat", background="#ccc")
    treeview = ttk.Treeview()
    trajectories = []
    for trajectory in selectedXyzFiles:
        XYZ = FileXYZ(trajectory)

        length = XYZ.fileLength
        linePerFrame = XYZ.chunkSize
        print(length, linePerFrame)

        numFrames = length // linePerFrame
        rest = length % linePerFrame
        print(numFrames, rest)

        firstIndex = treeview.insert("", tk.END, text=XYZ.name)
        trajectories.append(firstIndex)

        picoseconds = numFrames // 2000
        picoRange = list(range(0, picoseconds, 1))

        for picosecond in picoRange:
            picoSubTree = treeview.insert(firstIndex, tk.END, text=f"{picosecond}-{picosecond+1} ps")
            frameRange = list(range(picosecond*2000, (picosecond+1)*2000, 100))
            for frameInterval in frameRange:
                frameIntervalSubTree = treeview.insert(picoSubTree, tk.END, text=f"Frames [{frameInterval}:{frameInterval+99}]")
                for frame in range(frameInterval, frameInterval+100, 1):
                    treeview.insert(frameIntervalSubTree, tk.END, text=f"Frame {frame}")
        # for j in range(0, linePerFrame):
        #     line = treeview.insert(frame, tk.END, text=someSpeciation.getFrame(i*line))
    treeview.pack(side=tk.LEFT)
    button = ttk.Button(text="Print selection", command=printSelection)
    button.pack(side=tk.BOTTOM)
    root.mainloop()



    # print(someSpeciation.getPicosecond(0))
    # results = someSpeciation.getTimeSpeciation(2, 3)
    # writeFile(config.testFilesDir, results, "test")
    # print(results)
    # someSpeciation.printPicosecond(0)
    # test = range(0, 23840, 462)
    # print(list(test))

    # timestep = 0.5
    # for _ in range (0, length-linePerFrame, linePerFrame):
    #     print(_)
    #     pass

if __name__ == "__main__":
    main()