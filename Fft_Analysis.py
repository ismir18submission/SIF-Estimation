import Estimation
from pylab import *
import util
import Pitch


def analysis(audio_file, fft, tuning, config):
    if config.idmt:
        # normal frequency from audio
        normal_freq = Pitch.pitch_estimate(audio_file, config)
    else:
        # normal frequency from ground_truth
        normal_freq = util.get_normal_freq(audio_file, tuning)

    # determine weight of each estimation
    estimation_list = Estimation.init_estimations_from_normal(normal_freq, tuning, config)
    for estimation in estimation_list:
        w = weight(estimation, fft)
        estimation.set_weight(w)

    # init object
    estimation_result = Estimation.make_estimation()
    # find estimation with max weight
    for estimation in estimation_list:
        if estimation.weight > estimation_result.weight:
            estimation_result = estimation
    return estimation_result


def wnshs(freq, fft, normal_freq, no_partial):
    h = 0.84
    normalization = 0
    norm_sum = 0

    sh_sum = 0

    for partial in range(1, no_partial, 1):
        norm_sum += h ** (partial - 1)

        sh_value = (h ** (partial - 1)) * fft[freq * partial] * util.partial_dist(normal_freq, freq * partial)
        sh_sum += sh_value

    if norm_sum != 0:
        normalization = 1 / norm_sum

    sh_sum = normalization * sh_sum
    return sh_sum


def string_estimate(audio_file, fft, tuning, config):
    estimation = analysis(audio_file, fft, tuning, config)
    return estimation


def weight(estimation, fft):
    inverse_freq = estimation.inverse_freq
    normal_freq = estimation.normal_freq
    lower_scope, upper_scope = util.get_halftone_scope(inverse_freq)
    n_points = len(fft)

    scope_weights = []
    for scope_freq in range(lower_scope, upper_scope):
        no_partial = int(math.floor(n_points / scope_freq))
        scope_weight = wnshs(scope_freq, fft, normal_freq, no_partial)
        scope_weights.append(scope_weight)

    # maximum weight in the scope
    w = max(scope_weights)
    return w
