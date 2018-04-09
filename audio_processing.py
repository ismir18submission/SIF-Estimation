import math


def convert_pitch(pitch, p_type):
    if p_type.lower() == "hz":
        return math.pow(2, pitch / 12) * 440

    elif p_type.lower() == "midi":
        return int(round(12 * math.log(pitch / 440, 2)))


def idmt_preprocessing(a_s, s_r):
    a_s = a_s[0:s_r]
    a_s = a_s / (2. ** 15)
    return a_s, s_r


# array a_s:      audio_source
# int   s_r:      sample_rate
def pre_processing(a_s, s_r):
    a_s = a_s[0:s_r]

    a_s = a_s / (2. ** 15)
    a_s_left = a_s[:, 0]
    a_s_right = a_s[:, 1]
    return a_s_left, a_s_right, s_r
