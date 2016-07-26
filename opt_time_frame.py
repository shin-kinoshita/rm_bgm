from pydub import AudioSegment
import numpy as np
import math

#def get_sound_out_max_amp(sound_base, sound_adjust, move_arr):
#    max_amp_move = move_arr[0]
#    max_amp     = sound_base.overlay(get_sound_moved(sound_adjust, move_arr[0])).rms
#
#    for move in move_arr:
#        sound_moved = get_sound_moved(sound_adjust, move)
#        sound_over = sound_base.overlay(sound_moved)
#        print "move: " + str(move) + ", amp: " + str(sound_over.rms)
#        if sound_over.rms > max_amp:
#            max_amp_move = move
#            max_amp = sound_over.rms
#    
#    print "max_amp_move: " + str(max_amp_move) + ", max_amp: " + str(max_amp)
#
#    return get_sound_moved(sound_adjust, max_amp_move)


def get_sound_out_min_amp(sound_base, sound_adjust, move_arr):
    min_amp_move = move_arr[0]
    sound_over = sound_base + get_sound_moved(sound_adjust, move_arr[0])
    min_amp_x2 = np.dot(sound_over.astype(np.int64), sound_over.astype(np.int64))

    for move in move_arr:
        sound_over = sound_base + get_sound_moved(sound_adjust, move)
        amp_x2 = np.dot(sound_over.astype(np.int64), sound_over.astype(np.int64))
        print "move: " + str(move) + ", amp: " + str(amp_x2)
        if amp_x2 < min_amp_x2:
            min_amp_move = move
            min_amp_x2 = amp_x2
    
    print "min_amp_move: " + str(min_amp_move) + ", min_amp: " + str(min_amp_x2)

    return get_sound_moved(sound_adjust, min_amp_move)

def get_sound_moved(sound_base, move):

    dur_left  = 0
    dur_right = 0
    sound_trimmed = sound_base
    if move > 0:
        dur_left = np.abs(move)
        sound_trimmed = sound_base[0:-dur_left]
    elif move < 0:
        dur_right = np.abs(move) 
        sound_trimmed = sound_base[dur_right-1:-1]

    sound_sil_left  = np.array([0]*dur_left,  dtype=np.int16)
    sound_sil_right = np.array([0]*dur_right, dtype=np.int16)

    sound_moved = np.hstack([sound_sil_left, sound_trimmed, sound_sil_right])

    return sound_moved

def trans_audiosegment_to_array(audiosegment):
    array = audiosegment.get_array_of_samples()
    array = np.array(array, dtype=np.int16)

    return array

def trans_array_to_audiosegment(array, frame_rate, sample_width, channels):
    audiosegment = AudioSegment(
                        array.tobytes(),
                        frame_rate=frame_rate,
                        sample_width=sample_width,
                        channels=channels)
    return audiosegment

def main():
    f_format = "wav"

    sound_path_base   = "0321_base.wav"
    sound_path_adjust = "0321_delayinv.wav"
    sound_path_out    = "0321_delayinv_time.wav"

    sound_base   = AudioSegment.from_file(sound_path_base,   format=f_format)
    sound_adjust = AudioSegment.from_file(sound_path_adjust, format=f_format)

    f_rate  = sound_base.frame_rate
    s_width = sound_base.sample_width
    ch_num  = sound_base.channels

    max_move = -5000   # [dB]
    min_move = -20000  # [dB]
    move_arr = np.arange(min_move, max_move)
    
    sound_base_arr   = trans_audiosegment_to_array(sound_base)
    sound_adjust_arr = trans_audiosegment_to_array(sound_adjust)
    sound_out_arr    = get_sound_out_min_amp(sound_base_arr, sound_adjust_arr, move_arr)
    sound_out = trans_array_to_audiosegment(sound_out_arr, f_rate, s_width, ch_num)
    sound_out.export(sound_path_out, format=f_format)

if __name__ == '__main__':
    main()

