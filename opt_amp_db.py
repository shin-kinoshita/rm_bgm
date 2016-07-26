from pydub import AudioSegment
import numpy as np

def get_sound_out(sound_base, sound_adjust, mag_arr):
    min_amp_mag = mag_arr[0]
    min_amp     = sound_base.overlay(sound_adjust + mag_arr[0]).rms

    for mag in mag_arr:
        sound_over = sound_base.overlay(sound_adjust + mag)
        print "mag: " + str(mag) + ", amp: " + str(sound_over.rms)
        if sound_over.rms < min_amp:
            min_amp_mag = mag
            min_amp = sound_over.rms
    
    print "min_amp_move: " + str(min_amp_mag) + ", min_amp: " + str(min_amp)

    return sound_adjust + min_amp_mag

def main():
    f_format = "wav"

    sound_path_base   = "bake_adv.wav"
    sound_path_adjust = "bake_song_inv_timems.wav"
    sound_path_out    = "bake_song_inv_timems_amp.wav"

    sound_base   = AudioSegment.from_file(sound_path_base,   format=f_format)
    sound_adjust = AudioSegment.from_file(sound_path_adjust, format=f_format)

    max_ratio = -18      # [dB]
    min_ratio = -23      # [dB]
    step = 0.01
    mag_arr = np.arange(min_ratio, max_ratio, step)
    
    sound_out = get_sound_out(sound_base, sound_adjust, mag_arr)

    sound_out.export(sound_path_out, format=f_format)

if __name__ == '__main__':
    main()

