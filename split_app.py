# For the file dialog
import Tkinter as tk
from tkFileDialog import askopenfilename, askdirectory
from tkMessageBox import showinfo

# For the info output
import csv

# These are used to split audio and tell it's speech contents
from split_audio import split_file
from find_speech import vad_trial

# Used for formatting the file outputs
from math import log10, ceil

# This is the user-oriented function which
#       1. Asks the user for an audio file to process
#       2. Asks the user for an output directory
#       3. Splits the audio file into 1-minute chunks and puts them in the
#           output directory
#       4. Writes the percent of vocal content found in each file to a .csv
#           called config.csv in the output directory
def select_and_slice_file():
    # Tell the user what to do
    showinfo('Window', "Select an audio file to cut apart")
    # Get audio file
    audio_file = askopenfilename(
                        filetypes =(("Audio File", "*.wav"),("all files","*.*")),
                        title = "Please choose a .wav file."
                    )
    print(audio_file)

    # If no file is selected
    if audio_file == '':
        return False

    # Tell the user what to do
    showinfo('Window', "Select an output directory to save the audio chunks")

    # Select the output directory
    output_dir = askdirectory()
    print(output_dir)

    #if the output directory was not selected
    if output_dir == '':
        return False

    # Split audio file
    print("splitting file")
    filecount = split_file(audio_file, output_dir)

    # Run the Voice Activation Detector on each file
    percents = []

    print("vad_trial init")
    for file in range(filecount):
        filename = (output_dir+'/output%0'+str(ceil(log10(filecount)))+'d.wav')%file
        print("\t" + filename)
        percents.append([vad_trial(filename)])

    # Write the csv data log file
    print("writing the csv")
    with open(output_dir+"/config.csv", 'w') as output:
        writer = csv.writer(output)
        writer.writerows(percents)

# The running program
if __name__ == '__main__':
    # Make sure the general tk window does not appear
    tk.Tk().withdraw()
    # Run the program
    select_and_slice_file()
