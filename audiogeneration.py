import os
import wave
import time
from gensound import WAV
from gensound.curve import SineCurve
from gensound import Pan
from gensound import Gain
from pedalboard import Reverb, Pedalboard
from pedalboard.io import AudioFile
import subprocess


def generate_8D_Audio(audiofile, trimmed_file, freq_8D=0.075, amount_8D=100, reverb_room_size=0.1, reverb_damping=0, reverb_wet_level=0.33, reverb_dry_level=0.4, reverb_width=1):

    if '.mp3' in audiofile:
        subprocess.run(['ffmpeg', '-i', audiofile, 'converted.wav'])
        audiofile = 'converted.wav'

    if '.ogg' in audiofile:
        subprocess.run(['ffmpeg', '-i', audiofile, 'converted.wav'])
        audiofile = 'converted.wav'

    #Obtain audio file and its duration
    audio =  WAV(audiofile)
    audio_wav = wave.open(audiofile, 'rb')
    audio_duration = audio_wav.getnframes()/audio_wav.getframerate() #In Seconds

    #This is creates the actual 8D effect using SineCurve from the gensound library
    curve = SineCurve(frequency = freq_8D, depth = amount_8D, 
                      baseline = 0, duration = audio_duration * 1000)


    #Apply 8D panning and increase volume
    audio_8D = audio[0]*Pan(curve)
    audio_8D *= Gain(10)
    #Create The File
    audio_8D.export('Initial8D audiofile.wav', 
                    sample_rate=audio_wav.getframerate(),)
    
    #Add reverb to the 8D audio using the Pedalboard library
    board = Pedalboard([Reverb(room_size=reverb_room_size, damping=reverb_damping, wet_level=reverb_wet_level, dry_level=reverb_dry_level, width=reverb_width)])

    #Create the Reverb and 8D audio file
    with AudioFile('Initial8D audiofile.wav') as f:
    
        
        with AudioFile(f'8Dified {trimmed_file}', 'w', f.samplerate, f.num_channels) as o:
        
            
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
            
            
                effected = board(chunk, f.samplerate, reset=False)
            
            
                o.write(effected)

    #Remove original 8D audio file
    time.sleep(1)
    os.remove('Initial8D audiofile.wav')
    
