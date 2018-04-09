import Annotation
import math


def frequency(n, f):
    x = (f * (2 ** (float(n) / 12)))
    return x


def get_fret(fret_freq, empty_freq):
    return int(round(12 * math.log(fret_freq / empty_freq, 2)))


def get_halftone_scope(freq):
    upper_scope = float(freq) * (float(2) ** (float(1) / float(12)))
    lower_scope = float(freq) / (float(2) ** (float(1) / float(12)))
    return int(round(lower_scope)), int(round(upper_scope))


# given knowledge
def get_normal_freq(audio_file, tuning):
    return frequency(Annotation.from_wav(audio_file.name + ".wav").fret,
                     tuning.tuning[Annotation.from_wav(audio_file.name + ".wav").string - 1])


def in_scope(current_pitch, prev_pitch):
    lower_scope, upper_scope = get_halftone_scope(prev_pitch)
    return lower_scope <= current_pitch <= upper_scope


def inverse_frequency(n, f):
    return f / (1 - (2 ** (float(n - 1) / -12)))


def list_from_indexlist(list, index_list):
    temp = []
    for index in index_list:
        temp.append(list[index])
    return temp


def partial_dist(normal_freq, inv_freq):
    # a is the penalisation factor
    a = 100
    x = inv_freq
    y = normal_freq
    z = (x % y) / float(y)

    dist = min(z, 1 - z) * 2
    result = (dist / float(dist + a))
    return result
