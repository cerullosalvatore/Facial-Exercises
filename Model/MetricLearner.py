import itertools
import os
from pathlib import Path

import joblib
import numpy as np
from metric_learn import ITML, NCA, MLKR

from Model.observableObject import ObservableObject


class MetricLearner:
    def __init__(self):
        self._learner = None
        self._trained = ObservableObject(False)

    def train_metric_learner_supervised(self, landmark_fin_ok, landmark_fin_bad, path):

        landmarks = np.concatenate((landmark_fin_ok, landmark_fin_bad))
        landmarks = landmarks.reshape(landmarks.shape[0], landmarks.shape[1] * landmarks.shape[2])
        labels = []

        for i in range(len(landmark_fin_ok)):
            labels.append(1)
        for i in range(len(landmark_fin_bad)):
            labels.append(-1)

        self._learner = MLKR(preprocessor=landmarks)
        self._learner.fit(landmarks, labels)
        self.save_learner(path)


    def train_metric_learner_supervised_all_landmarks(self, landmark_init_ok, landmark_fin_ok, landmark_fin_bad, path):
        landmarks = np.concatenate((landmark_init_ok, landmark_fin_ok, landmark_fin_bad))
        landmarks = landmarks.reshape(landmarks.shape[0], landmarks.shape[1] * landmarks.shape[2])
        labels = []

        for i in range(len(landmark_init_ok)):
            labels.append(0)
        for i in range(len(landmark_fin_ok)):
            labels.append(1)
        for i in range(len(landmark_fin_bad)):
            labels.append(-1)

        # Utilizzo anche i video corretti degli altri esercizi
        for categoria in os.listdir("Exercises"):
            cat_path = Path("Exercises/" + categoria)
            if cat_path.is_dir():
                for name in os.listdir(cat_path):
                    ex_path = Path("Exercises/" + categoria + "/" + name)
                    if ex_path.is_dir() and ex_path != Path(path):
                        pathCorrect = Path("Exercises/" + categoria + "/" + name + "/Correct")
                        for file in os.listdir(pathCorrect):
                            if file.endswith(".npy"):
                                pathFile= str(pathCorrect) + "\\" + file
                                landmark = np.load(pathFile , allow_pickle=True)[38].reshape(1, 68*2)
                                landmarks = np.concatenate((landmarks, landmark))
                                labels.append(-1)

        self._learner = MLKR(preprocessor=landmarks)
        self._learner.fit(landmarks, labels)
        self.save_learner(path)

    def get_learner(self):
        return self._learner

    def save_learner(self, path):
        joblib.dump(self._learner, path + "TreanedModel.sav")

    def load_learner(self, path):
        self._learner = joblib.load(path + "TreanedModel.sav")

    def remove_learner(self, path):
        os.remove(path + ".sav")
