import Smile
import numpy as np
import os


def mfcc(audio_files, annotations, config):
    X = []
    for a_f in audio_files:
        file_name = a_f.name
        file_path = a_f.path

        if not os.path.isfile(config.mfcc_output_path + file_name + '.csv'):
            Smile.extract_ops_features(file_name, file_path, config.mfcc_config_file, config.mfcc_output_path)
        file = open(config.mfcc_output_path + file_name + '.csv', 'rb')

        # parse data
        data = file.read().replace('\n', '').replace('\r', ';').split(';')
        data = data[:-1]

        temp = []
        for value in data:
            try:
                value = float(value)
                temp.append(value)
            except ValueError:
                pass
        data = [temp]
        X.extend(data)

    y = []
    for annotation in annotations:
        label = []
        for i in range(0, len(data)):
            label.append(annotation.string)
        y.extend(label)
    X = np.array(X)
    y = np.array(y)
    return X, y
