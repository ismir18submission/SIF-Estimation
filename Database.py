from scipy.io import wavfile
import os
import audio_processing as ap
import Annotation
import Audio
import xml.etree.ElementTree
import Tuning


class Database:
    audio_files = []
    annotations = []
    tuning = []

    def __init__(self, aud_f, ann_f, t):
        self.audio_files = aud_f
        self.annotations = ann_f
        self.tuning = t


# annotation and audio files must have the same name
def load_database(config):
    audio_path = config.audio_path
    annotation_path = config.annotation_path
    tuning_path = config.tuning_path
    audio_files = []
    annotations = []
    tuning_files = []

    # AUDIO ------------------------------------
    if config.idmt:
        for filename in os.listdir(audio_path):
            if filename.endswith(".wav"):
                sample_rate, audio_source = wavfile.read(os.path.join(audio_path, filename))
                a_s, s_r = ap.idmt_preprocessing(audio_source, sample_rate)
                audio_file = Audio.make_audio(a_s, a_s, s_r, filename, audio_path)
                audio_files.append(audio_file)
            else:
                continue
    else:
        for string in range(1, config.no_strings + 1):
            string_path = audio_path + str(string)
            for filename in os.listdir(string_path):
                if filename.endswith(".wav"):
                    sample_rate, audio_source = wavfile.read(os.path.join(string_path, filename))
                    a_s_left, a_s_right, s_r = ap.pre_processing(audio_source, sample_rate)
                    audio_file = Audio.make_audio(a_s_left, a_s_right, s_r, filename, string_path)
                    audio_files.append(audio_file)
                else:
                    continue

    # ANNOTATION ------------------------------------
    if config.idmt:
        for filename in os.listdir(annotation_path):
            if filename.endswith(".xml"):
                root = xml.etree.ElementTree.parse(os.path.join(annotation_path, filename)).getroot()
                annotation = Annotation.from_xml(root)
                annotations.append(annotation)
            else:
                continue
    else:
        for string in range(1, config.no_strings + 1):
            string_path = annotation_path + str(string)
            for filename in os.listdir(string_path):
                if filename.endswith(".wav"):
                    annotation = Annotation.from_wav(filename)
                    annotations.append(annotation)
                else:
                    continue

    # TUNING ------------------------------------
    if config.idmt:
        for annotation in annotations:
            if annotation.fret == 0:
                for a_f in audio_files:
                    if a_f.name == annotation.filename:
                        tuning_files.append(a_f)
    else:
        for filename in os.listdir(tuning_path):
            if filename.endswith(".wav"):
                sample_rate, audio_source = wavfile.read(os.path.join(tuning_path, filename))
                a_s_left, a_s_right, s_r = ap.pre_processing(audio_source, sample_rate)
                audio_file = Audio.make_audio(a_s_left, a_s_right, s_r, filename, tuning_path)
                tuning_files.append(audio_file)
            else:
                continue
    tuning = Tuning.estimate_tuning(tuning_files, config)

    # Filter based on fret-range
    audio_temp = []
    annotation_temp = []
    # audio filter
    for a_f in audio_files:
        for annotation in annotations:
            if a_f.name == annotation.filename:
                if config.max_fret >= annotation.fret >= config.min_fret:
                    audio_temp.append(a_f)
                    annotation_temp.append(annotation)
    audio_files = audio_temp
    annotations = annotation_temp

    # RETURN ------------------------------------
    return Database(audio_files, annotations, tuning)
