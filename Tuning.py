import Pitch


class Tuning:
    tuning = []

    def __init__(self, t):
        self.tuning = t


def estimate_tuning(audio_files, config):
    tuning = []

    for audio_file in audio_files:
        pitch = Pitch.pitch_estimate(audio_file, config)
        tuning.append(pitch)

    return Tuning(tuning)
