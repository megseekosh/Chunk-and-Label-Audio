from pydub import AudioSegment
from pydub.utils import mediainfo

from math import ceil, log10

# Split file
# source_file is the filename of the audio we will be splitting
def split_file(source_file, output_directory="output"):
    # This is the audio input which we will be splitting
    sound = AudioSegment.from_file(source_file)

    # This is metadata about the file we will be splitting
    data = mediainfo(source_file)

    # This is a conversaion factor used to cut apart the audio into one minute
    #  chunks. Often sample_rate given can be slightly off, so I decided to use
    #  a more base approach, dividing the length (samples) by the duration (seconds)
    #  and scaling up by a factor of 60 (seconds per minute)
    samples_per_minute = int(60*len(sound)/float(data["duration"]))

    # Get log_base_10 of number of minutes in the file to figure out how long
    #  the filename ids must be. If it is between 10 and 99 then all outputs
    #  must be formatted to length 2, i.e. 00, 01, 02... 10, 11, 12... 97, 98, 99
    name_size = ceil(log10(float(data["duration"])/60))

    # Number of minutes in the file, rounded upwards
    minutes = int(ceil(float(len(sound))/samples_per_minute))

    # Loop through every minute of the audio and output it into the folder
    #  output as "output{n}.wav" where {n} = the minute id (starts at minute 0)
    output_format = "%s/output%0"+str(name_size)+"d.wav"

    for i in range(minutes):
        print("\t"+output_format % (output_directory, i))
        split_sound = sound[i*samples_per_minute:(i+1)*samples_per_minute]
        split_sound.export( output_format % (output_directory, i),
                            format="wav",
                            bitrate=data["bit_rate"])

    return minutes
