from pydub import AudioSegment
import numpy as np
import math

def main():
    f_format = "wav"

    sound_path_base   = "bake_song.wav"
    sound_path_out    = "bake_song_inv.wav"

    sound_base = AudioSegment.from_file(sound_path_base, format=f_format)

    sound_out = sound_base.invert_phase()

    sound_out.export(sound_path_out, format=f_format)

if __name__ == '__main__':
    main()

