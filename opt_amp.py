from pydub import AudioSegment
import numpy as np

def get_sound_out_min_amp(sound_base, sound_adjust, mag_arr):
    sound_len    = min(len(sound_base), len(sound_adjust))
    sound_base   = sound_base[:sound_len]
    sound_adjust = sound_adjust[:sound_len]

    min_amp_mag = mag_arr[0]
    sound_over = sound_base + sound_adjust * mag_arr[0]
    min_amp_x2 = np.dot(sound_over.astype(np.int64), sound_over.astype(np.int64))

    for mag in mag_arr:
        sound_over = sound_base + sound_adjust * mag
        amp_x2 = np.dot(sound_over.astype(np.int64), sound_over.astype(np.int64))
        print "mag: " + str(mag) + ", amp: " + str(amp_x2)
        if amp_x2 < min_amp_x2:
            min_amp_mag = mag
            min_amp_x2 = amp_x2
    
    print "min_amp_move: " + str(min_amp_mag) + ", min_amp: " + str(min_amp_x2)

    return np.array(sound_adjust * min_amp_mag, dtype=np.int16)

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

    sound_path_base   = "bake_adv.wav"
    sound_path_adjust = "bake_song_inv_timems.wav"
    sound_path_out    = "bake_song_inv_timems_amp.wav"

    sound_base   = AudioSegment.from_file(sound_path_base,   format=f_format)
    sound_adjust = AudioSegment.from_file(sound_path_adjust, format=f_format)

    f_rate  = sound_base.frame_rate
    s_width = sound_base.sample_width
    ch_num  = sound_base.channels

    max_ratio = 0.10     # no unit
    min_ratio = 0.07     # no unit
    step = 0.0001
    mag_arr = np.arange(min_ratio, max_ratio, step)
    
    sound_base_arr   = trans_audiosegment_to_array(sound_base)
    sound_adjust_arr = trans_audiosegment_to_array(sound_adjust)
    sound_out_arr    = get_sound_out_min_amp(sound_base_arr, sound_adjust_arr, mag_arr)
    sound_out = trans_array_to_audiosegment(sound_out_arr, f_rate, s_width, ch_num)
    sound_out.export(sound_path_out, format=f_format)

if __name__ == '__main__':
    main()

