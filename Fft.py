from pylab import *


def make_fft(audio_source):
    n = len(audio_source)
    p = fft(audio_source)  # take the fourier transform

    nUniquePts = int(ceil((n + 1) / 2.0))
    p = p[0:nUniquePts]
    p = abs(p)

    p = p / float(n)
    p = p ** 2

    # odd number of points fft
    if n % 2 > 0:
        p[1:len(p)] = p[1:len(p)] * 2
    else:
        # even number of points fft
        p[1:len(p) - 1] = p[1:len(p) - 1] * 2

    return p
