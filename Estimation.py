import util


class Estimation:
    string = 0
    fret = 0
    weight = 0
    normal_freq = 0
    inverse_freq = 0

    def __init__(self, s, f, n_f, i_f):
        self.string = s
        self.fret = f
        self.normal_freq = n_f
        self.inverse_freq = i_f
        self.weight = 0

    def set_weight(self, weight):
        self.weight = weight

    def __eq__(self, other):
        return self.string == other.string and self.fret == other.fret


def estimations_from_predictions(predictions, annotations, tuning, config):
    e_list = []
    for prediction, annotation in zip(predictions, annotations):
        string = annotation.string
        fret = annotation.fret
        normal_freq = util.frequency(fret, tuning.tuning[string - 1])

        estimations = init_estimations_from_normal(normal_freq, tuning, config)
        string = 1
        for confidence in prediction:
            for estimation in estimations:
                if estimation.string == string:
                    estimation.set_weight(confidence)

            string += 1

        # init estimation object with weight = 0
        e = make_estimation()
        # find estimation with max weight
        for estimation in estimations:
            if estimation.weight > e.weight:
                e = estimation
        e_list.append(e)
    return e_list


def init_estimations_from_normal(normal_freq, tuning, config):
    estimations_list = []
    i = 1
    for empty_string_freq in tuning.tuning:
        if normal_freq >= empty_string_freq:
            fret = util.get_fret(normal_freq, empty_string_freq)
            string = i
            # check if fret is in fret-range
            if config.min_fret <= fret <= config.max_fret:
                inverse_freq = util.inverse_frequency(fret, empty_string_freq)
                estimations_list.append(Estimation(string, fret, normal_freq, inverse_freq))
        i += 1
    return estimations_list


def hybrid_estimation(mfcc, sif, config):
    th = config.confidence_th
    if mfcc.weight >= th:
        result = mfcc
    else:
        result = sif
    return result


def make_estimation(s=0, f=0, n_f=0, i_f=0):
    return Estimation(s, f, n_f, i_f)
