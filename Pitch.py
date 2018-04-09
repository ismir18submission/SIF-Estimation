import Smile
from pylab import *
import csv
import Candidate
import os


def pitch_estimate(audio_file, config):
    file_name = audio_file.name
    audio_path = audio_file.path
    ops_output_path = config.ops_output_path
    ops_config_path = config.ops_config_path
    feature_path = ops_output_path + file_name + '.csv'

    # openSmile pitch estimation
    if not os.path.isfile(feature_path):
        Smile.extract_ops_features(file_name, audio_path, ops_config_path, ops_output_path)

    # read csv file created by openSmile
    with open(feature_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')

        # interpret pitch
        pitch_values = []
        first = True
        # for each pitch-value in time-window
        for row in reader:
            # ignore first row in reader
            if not first:
                pitch_value = int(round(float(row[2])))
                pitch_values.append(pitch_value)
            first = False
    pitch = Candidate.find_pitch_candidate(pitch_values, config.min_freq)
    return pitch
