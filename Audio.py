class Audio:
    audio_source_l = []
    audio_source_r = []
    sample_rate = 0
    name = ""
    path = ""

    def __init__(self, a_s_l, a_s_r, s_r, name, path):
        self.audio_source_l = a_s_l
        self.audio_source_r = a_s_r
        self.sample_rate = s_r
        self.name = name[:-4]
        self.path = path


def make_audio(a_s_l, a_s_r, s_r, name, path):
    audio = Audio(a_s_l, a_s_r, s_r, name, path)
    return audio
