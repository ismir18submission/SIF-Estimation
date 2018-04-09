import Database
import Fft_Analysis
import Fft
import Annotation
import Estimation
import Mfcc
from sklearn.model_selection import StratifiedKFold
from sklearn import svm
from sklearn import calibration
import util


def sif_main(config):
    database = Database.load_database(config)
    audio_files = database.audio_files

    estimations = []
    for audio_file in audio_files:
        # take left audio source
        audio_source = audio_file.audio_source_l
        tuning = database.tuning

        fft = Fft.make_fft(audio_source)
        estimation = Fft_Analysis.string_estimate(audio_file, fft, tuning, config)
        estimations.append(estimation)

    return estimations


def mfcc_main(config):
    database = Database.load_database(config)

    audio_files = database.audio_files
    tuning = database.tuning

    annotations = database.annotations
    X, y = Mfcc.mfcc(audio_files, annotations, config)

    for c in [10 ** x for x in range(-6, 1, 1)]:

        # 10 fold cross-validation
        kf = StratifiedKFold(n_splits=10, shuffle=True)
        for train, test in kf.split(X, y):
            X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
            my_svm = svm.LinearSVC(C=c, tol=1e-3)
            clf = calibration.CalibratedClassifierCV(my_svm)

            clf.fit(X_train, y_train)

            predictions = clf.predict_proba(X_test)

            annotations_test = Annotation.from_indexlist(annotations, test)
            estimations = Estimation.estimations_from_predictions(predictions, annotations_test, tuning, config)

    return estimations


def hybrid_main(config):
    database = Database.load_database(config)
    sif_estimation_list = sif_main(config)
    audio_files = database.audio_files
    tuning = database.tuning

    annotations = database.annotations
    X, y = Mfcc.mfcc(audio_files, annotations, config)

    for c in [10 ** x for x in range(-6, 1, 1)]:
        # 10 fold cross-validation
        kf = StratifiedKFold(n_splits=10, shuffle=True)

        for train, test in kf.split(X, y):
            X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]
            my_svm = svm.LinearSVC(C=c, tol=1e-3)
            clf = calibration.CalibratedClassifierCV(my_svm)

            clf.fit(X_train, y_train)

            predictions = clf.predict_proba(X_test)

            annotations_test = Annotation.from_indexlist(annotations, test)
            mfcc_estimations = Estimation.estimations_from_predictions(predictions, annotations_test, tuning, config)
            sif_estimations = util.list_from_indexlist(sif_estimation_list, test)

            hybrid_estimations = []
            for m_e, s_e in zip(mfcc_estimations, sif_estimations):
                hybrid_estimation = Estimation.hybrid_estimation(m_e, s_e, config)
                hybrid_estimations.append(hybrid_estimation)

    return hybrid_estimations
