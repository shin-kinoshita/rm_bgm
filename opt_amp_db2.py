from pydub import AudioSegment
import numpy as np

def get_sound_out(sound_base, sound_adjust, mag_arr, window):
    sound_base_parts   = [sound_base[i:i+window]   for i in range(0, len(sound_base),   window)]
    sound_adjust_parts = [sound_adjust[i:i+window] for i in range(0, len(sound_adjust), window)]

    sound_out = AudioSegment.empty()
    for i in range(len(sound_base_parts)):
        sound_out_part = get_sound_part(sound_base_parts[i], sound_adjust_parts[i], mag_arr)
        sound_out += sound_out_part

    return sound_out

def get_sound_part(sound_base, sound_adjust, mag_arr):
    min_amp_mag = mag_arr[0]
    min_amp     = sound_base.overlay(sound_adjust + mag_arr[0]).rms

    for mag in mag_arr:
        sound_over = sound_base.overlay(sound_adjust + mag)
        #print "mag: " + str(mag) + ", amp: " + str(sound_over.rms)
        if sound_over.rms < min_amp:
            min_amp_mag = mag
            min_amp = sound_over.rms
    
    print "min_amp_mag: " + str(min_amp_mag) + ", min_amp: " + str(min_amp)

    return sound_adjust + min_amp_mag

    
def main():
    f_format = "wav"

    sound_path_base   = "bake_adv.wav"
    sound_path_adjust = "bake_song_inv_timems.wav"
    sound_path_out    = "bake_song_inv_timems_amp2.wav"

    sound_base   = AudioSegment.from_file(sound_path_base,   format=f_format)
    sound_adjust = AudioSegment.from_file(sound_path_adjust, format=f_format)

    max_ratio = -5       # [dB]
    min_ratio = -30      # [dB]
    step = 0.01
    mag_arr = np.arange(min_ratio, max_ratio, step)
    
    window = 500         # [ms]

    sound_out = get_sound_out(sound_base, sound_adjust, mag_arr, window)

    sound_out.export(sound_path_out, format=f_format)

if __name__ == '__main__':
    main()

