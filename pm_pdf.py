import sys
import tkinter as tk
import tkinter.ttk as ttk
import os
import subprocess
import glob
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image, ImageTk

path = "./paper"
files = glob.glob(path + "/*")

poppler_dir = Path(sys.argv[0]).parent.absolute() / "poppler/bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)

'''
frame and grids
________________
|1   |3   |5   |
|____|____|____|
|2___|4___|6___|

'''
window_width = 1400
window_height = 750
column1_width = 300
column2_width = 800
column3_width = 300

filename = "paper/test.pdf"  # just for test
img = Image.open("image/image.png")

def btn_update_click():
    print("update")

def menu_bar(e):
    menubar = tk.Menu(e)
    filemenu = tk.Menu(menubar, tearoff = 0)
    filemenu.add_command(label="Menu1")
    filemenu.add_command(label="Menu2")
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=e.quit)
    
    helpmenu = tk.Menu(menubar, tearoff = 0)
    helpmenu.add_command(label="help")
    helpmenu.add_command(label="version")

    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Help", menu=helpmenu)
    e.config(menu=menubar)

def create_pdf_preview(filename):
    path = Path(sys.argv[0]).parent.absolute() / ("./paper/" + filename + ".pdf")
    pages = convert_from_path(Path(path),25, last_page=1)
    savepath = "image/" + filename + ".png"
    pages[0].save(Path(sys.argv[0]).parent.absolute() / savepath, "png")

def open_pdf(e):
    
    """
        open pdf file on chrome
    """
    file = os.path.abspath(filename)
    subprocess.run([file], shell=True)

def print_on_subframe2(data):
    sub2_txt.delete('1.0', 'end')
    sub2_txt.insert(tk.END, data)

def tree_selected(event):
    for item in tree.selection():
        title_tuple = tree.item(item, "values")
        print_on_subframe2(title_tuple[1])

        global filename
        filename = path + "/" + title_tuple[1] + ".pdf"

        global img
        img_path = "./image/" + title_tuple[1] + ".png"
        print(img_path)

        if os.path.isfile(img_path):
            img = Image.open(img_path)
            canvas.delete("img")
            canvas.Photo = ImageTk.PhotoImage(img)
            canvas.create_image(0,0, image=canvas.Photo, anchor=tk.NW, tag="img")
        else:
            create_pdf_preview(title_tuple[1])
            img = Image.open(img_path)
            canvas.delete("img")
            canvas.Photo = ImageTk.PhotoImage(img)
            canvas.create_image(0,0, image=canvas.Photo, anchor=tk.NW, tag="img")

root = tk.Tk()
root.title("paper manager")
root.geometry(str(window_width)+"x"+str(window_height))


iconfile = './favicon.ico'
root.iconbitmap(default=iconfile)

menu_bar(root)

frame_1=ttk.Frame(root, width=column1_width, height="700", relief="ridge")
frame_2=ttk.Frame(root, width=column2_width, height="700", relief="ridge")
frame_3=ttk.Frame(root, width=column3_width, height="700", relief="ridge")
frame_4=ttk.Frame(root, width="1400", height="50", relief="ridge")


frame_1.grid(row=0, column=0)
frame_2.grid(row=0, column=1)
frame_3.grid(row=0, column=2)
frame_4.grid(row=1, columnspan=3)

frame_1.propagate(False)
frame_2.propagate(False)
frame_3.propagate(False)

root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

subframe_1=ttk.Frame(frame_1, width="300", height="400", relief="ridge")
subframe_2=ttk.Frame(frame_1, width="300", height="300", relief="ridge")
subframe_3=ttk.Frame(frame_2, width="800", height="700", relief="ridge")
subframe_4=ttk.Frame(frame_2, width="800", height="250", relief="ridge")
subframe_5=ttk.Frame(frame_3, width="300", height="300", relief="ridge")
subframe_6=ttk.Frame(frame_3, width="300", height="400", relief="ridge")


### subframe_2 messege text output
sub2_word = 'description'
sub2_txt = tk.Text(subframe_2)
sub2_txt.pack(padx=2, pady=2)
sub2_txt.insert(tk.END, sub2_word)
### end of subframe_2


### subframe_3 Paper List Tree View
tree = ttk.Treeview(subframe_3)

scroll = ttk.Scrollbar(subframe_3, orient="vertical", command=tree.yview)
scroll.pack(side="right", fill="y")

tree.configure(yscrollcommand=scroll.set)

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

tree.bind("<<TreeviewSelect>>", tree_selected)
tree.bind("<Double-Button-1>", open_pdf)

tree.pack(padx=5, pady=5, fill=tk.BOTH, expand=1)
### end of subframe_3


### subframe_5 pdf preview
canvas = tk.Canvas(subframe_5, width = img.width, height = 280)
canvas.pack(padx=5, pady=5)
canvas.Photo = ImageTk.PhotoImage(img)
canvas.create_image(0,0, image=canvas.Photo, anchor=tk.NW, tag="img")
### end of subframe_5

button1 = tk.Button(subframe_1, text="exit", command=root.quit)
button1.pack(padx=5, pady=5)

subframe_1.grid(row=0, column=0)
subframe_2.grid(row=1, column=0)
subframe_3.grid(row=0, column=0, sticky=tk.W+tk.E)
#subframe_4.grid(row=1, column=0)
subframe_5.grid(row=0, column=0)
subframe_6.grid(row=1, column=0)


subframe_1.propagate(False)
subframe_2.propagate(False)
subframe_3.propagate(False)
subframe_4.propagate(False)
subframe_5.propagate(False)
subframe_6.propagate(False)

root.mainloop()