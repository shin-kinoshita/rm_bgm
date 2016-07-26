from pydub import AudioSegment
import numpy as np
import math

def get_sound_out_max_amp(sound_base, sound_adjust, move_arr):
    max_amp_move = move_arr[0]
    max_amp     = sound_base.overlay(get_sound_moved(sound_adjust, move_arr[0])).rms

    for move in move_arr:
        sound_moved = get_sound_moved(sound_adjust, move)
        sound_over = sound_base.overlay(sound_moved)
        print "move: " + str(move) + ", amp: " + str(sound_over.rms)
        if sound_over.rms > max_amp:
            max_amp_move = move
            max_amp = sound_over.rms
    
    print "max_amp_move: " + str(max_amp_move) + ", max_amp: " + str(max_amp)

    return get_sound_moved(sound_adjust, max_amp_move)


def get_sound_out_min_amp(sound_base, sound_adjust, move_arr):
    min_amp_move = move_arr[0]
    min_amp     = sound_base.overlay(get_sound_moved(sound_adjust, move_arr[0])).rms

    for move in move_arr:
        sound_moved = get_sound_moved(sound_adjust, move)
        sound_over = sound_base.overlay(sound_moved)
        print "move: " + str(move) + ", amp: " + str(sound_over.rms)
        if sound_over.rms < min_amp:
            min_amp_move = move
            min_amp = sound_over.rms
    
    print "min_amp_move: " + str(min_amp_move) + ", min_amp: " + str(min_amp)

    return get_sound_moved(sound_adjust, min_amp_move)

def get_sound_moved(sound_base, move):

    dur_left  = 0
    dur_right = 0
    sound_trimmed = sound_base
    if move > 0:
        dur_left = math.fabs(move)
        sound_trimmed = sound_base[0:-dur_left]
    elif move < 0:
        dur_right = math.fabs(move) 
        sound_trimmed = sound_base[dur_right-1:-1]

    sound_sil_left  = AudioSegment.silent(duration=dur_left)
    sound_sil_right = AudioSegment.silent(duration=dur_right)

    sound_moved = sound_sil_left + sound_trimmed + sound_sil_right

    return sound_moved

def main():
    f_format = "wav"

    sound_path_base   = "bake_adv.wav"
    sound_path_adjust = "bake_song_inv.wav"
    sound_path_out    = "bake_song_inv_timems.wav"

    sound_base   = AudioSegment.from_file(sound_path_base,   format=f_format)
    sound_adjust = AudioSegment.from_file(sound_path_adjust, format=f_format)

    max_move = -500     # [ms]
    min_move = -1500    # [ms]
    move_arr = np.arange(min_move, max_move)
    
    sound_out = get_sound_out_min_amp(sound_base, sound_adjust, move_arr)

    sound_out.export(sound_path_out, format=f_format)

if __name__ == '__main__':
    main()

