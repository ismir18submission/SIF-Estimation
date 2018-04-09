class Config(object):

    ops_config_path = 'pitch_loudness_shs.conf'
    ops_output_path = 'pitch_annotation/'

    mfcc_config_file = 'mfcc_func.conf'
    mfcc_output_path = 'mfcc/'

    audio_path = ""
    annotation_path = ""
    window_size = 0
    hop_size = 0
    tuning_path = ""

    is_guitar = False
    is_bass = not is_guitar
    guitar_min_freq = 80
    bass_min_freq = 40

    no_guitar_strings = 6
    no_bass_strings = 4

    no_strings = 0

    min_freq = 0
    max_fret = 14
    min_fret = 3

    excitation_th = 0
    estimation_th = 0

    confidence_th = 0.35

    idmt = False

    string_names = []

    def __init__(self, adp, anp, tp, g, xt, min_fret, max_fret, ws=10000, hs=128, idmt=False):
        self.audio_path = adp
        self.annotation_path = anp
        self.window_size = ws
        self.hop_size = hs
        self.is_guitar = g
        self.is_bass = not self.is_guitar
        self.excitation_th = xt
        self.idmt = idmt
        self.min_fret = min_fret
        self.max_fret = max_fret

        if not idmt:
            self.tuning_path = tp
        else:
            self.tuning_path = []

        if self.is_guitar:
            self.min_freq = self.guitar_min_freq
            self.no_strings = self.no_guitar_strings
            self.string_names = ['E', 'A', 'D', 'G', 'B', 'e', ]
        else:
            self.min_freq = self.bass_min_freq
            self.no_strings = self.no_bass_strings
            self.string_names = ['E', 'A', 'D', 'G']


def make_config(config_string, idmt=False):
    if not idmt:
        adp = 'Datasets/SIF-Database/' + config_string + '/Samples/String_'
        anp = 'Datasets/SIF-Database/' + config_string + '/Samples/String_'
        tp = 'Datasets/SIF-Database/' + config_string + '/Tuning'
        g = config_string.split('_')[0] != "bass"
        xt = 0
        min_fret = 3
        max_fret = 12
    else:
        adp = 'Datasets/IDMT-SMT-GUITAR/dataset1/' + config_string + '/audio'
        anp = 'Datasets/IDMT-SMT-GUITAR/dataset1/' + config_string + '/annotation'
        tp = []
        g = True
        xt = 0
        min_fret = 3
        max_fret = 12
    return Config(adp, anp, tp, g, xt, min_fret, max_fret, idmt=idmt)
