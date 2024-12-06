import tkinter as tk
from tkinter import ttk

from Classes.Chemistry.Molecule import Molecule


class InteractiveSpeciation():
    def __init__(self, recursiveItem):

        self.window = tk.Tk()
        self.window.title("Explore speciation")
        self.window.geometry("1024x768")

        self.treeviewFrame = ttk.Frame(self.window)
        self.treeviewFrame.place(x=0, y=0, relwidth=0.3, relheight=1)   
        
        
        self.showcaseFrame = ttk.Frame(self.window)
        self.showcaseFrame.place(relx=0.3, y=0, relwidth=0.7, relheight=1)

        # self.treeviewFrame.pack()
        # self.showcaseFrame.pack()
        # self.currentPlot = tk.StringVar()
        self.showcaseTitle = ttk.Label(self.showcaseFrame, text="Start")
        self.showcasePlot = ttk.Label(self.showcaseFrame, text="Plot")
        # self.showcaseTitle['textvariable'] = self.currentPlot
        self.showcaseTitle.pack()
        self.showcasePlot.pack()



        self.treeview = ttk.Treeview(self.treeviewFrame)
        self.treeview.tag_bind("selected", "<<TreeviewSelect>>", self.itemSelected)
        self.globalIndexes = {}
        self.recursiveExploration(recursiveItem)
        self.treeview.pack()
        

        
        self.window.mainloop()

    # This function should be reversed, so that the treeview is built from the bottom up
    # to ensure compatibility with Composite Design Pattern
    def recursiveExploration(self, parent):
        iid = self.treeview.insert("", "end", text = parent.__repr__(), values=parent, tags=("selected",))
        if parent.__class__.__name__ == "AtomicSystem":
            Molecule.atomicSystemSize = parent.size
        self.globalIndexes[iid] = parent
        try: 
            for child in parent.children:
                childIid = self.recursiveExploration(child)
                self.treeview.move(childIid, iid, "end")
        except AttributeError:
            try:
                for child in parent:
                    childIid = self.recursiveExploration(child)
                    self.treeview.move(childIid, iid, "end")
            except TypeError:
                pass
        return iid

        # if item.isLeaf():
        #     self.treeview.insert("", "end", text=item.__repr__())
        # else:
        #     for subItem in item:
        #         self.recursiveExploration(subItem)

    def itemSelected(self, event):
        selectedItem = self.treeview.selection()[0]
        newTitle = self.globalIndexes[selectedItem].__repr__()
        newPlot = self.globalIndexes[selectedItem].plot()
        # newTitle = self.treeview.item(selectedItem, option="text")
        # newPlot = self.treeview.item(selectedItem, option="values")
        # print(newTitle, type(newTitle))
        # print(newPlot, type(newPlot))
        # self.currentPlot.set(self.treeview.item(selectedItem, option="text"))
        self.showcaseTitle.configure(text=newTitle)
        self.showcasePlot.configure(text=newPlot)