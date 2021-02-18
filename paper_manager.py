import sys
import tkinter as tk
import tkinter.ttk as ttk
import os
import glob

path = "./paper"
files = glob.glob(path + "/*")

root = tk.Tk()
root.title("paper manager")
root.geometry("800x500")

label = tk.Label(root, text=path)
label.pack()

tree = ttk.Treeview(root)

tree["columns"] = (1,2,3)
tree["show"] = "headings"

tree.column(1, width=40)
tree.column(2, width=600)
tree.column(3, width=100)

tree.heading(1, text="index")
tree.heading(2, text="title")
tree.heading(3, text="type")

for i,file in enumerate(files):
    basename = os.path.splitext(os.path.basename(file))[0]
    extention = os.path.splitext(file)[1][1:]
    tree.insert("", "end", value=(i, basename, extention))

tree.pack()


Button = tk.Button(text="quit", command=root.quit)
Button.pack()

root.mainloop()