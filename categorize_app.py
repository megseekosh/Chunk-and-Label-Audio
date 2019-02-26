from Tkinter import *
import ttk

from tkFileDialog import askdirectory
from tkMessageBox import showinfo

from math import ceil, log10

#current filenumber
filenumber = 0
#number of minute-audio-clips in folder
filecount = 0

#convert file number and file count to file name
def to_filename(filenumber, filecount):
    format = "output%0"+str(ceil(log10(filecount)))+"d"
    return format%(filenumber)

#play the current audio file aloud
def play_audio(folder, filenumber, filecount):
    format = "open %s/%s"%(folder, to_filename(filenumber, filecount))

    system(format%(folder, filenumber))

#go to the next audio file
def next_audio():
    pass

if __name__ == "__main__":
    root = Tk()

    showinfo('Window', "Select a directory to categorize")

    file = askdirectory()

    #use config file to get file info
    with open(file+"/config.csv", "r") as f:
        for line in f:
            filecount += 1

    root.update()

    # setup window
    root.title("Categorize")

    frame = Frame(root, bg="white")

    frame.grid(row=4, column=3)

    category = StringVar()

    Button(frame, background="gray", text="Play Audio", command=play_audio).grid(row=1, column=1)

    choices = {"Quechua", "Spanish", "Quechua and Spanish", "Neither"}

    category.set("Categorize me")

    popupMenu = OptionMenu(frame, category, *choices)

    popupMenu.grid(row=3, column=1)

    Label(frame, text="Child Speech: ").grid(row = 3, column = 0)

    Label(frame, text=".../%s"%to_filename(filenumber, filecount)).grid(row = 0, column = 1)

    Button(frame, text="Next", command=next_audio, bg="gray").grid(row=3, column=2)

    root.mainloop()
