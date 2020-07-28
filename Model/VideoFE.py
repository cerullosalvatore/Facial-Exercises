import cv2
import numpy as np

class VideoFE():
    def __init__(self, name):
        self._name = name
        self._landmarks = []

    def get_landmarks(self):
        return self._landmarks

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def set_landmarks(self, landmarks):
        self._landmarks = landmarks

    def insert_landmark(self, landmark):
        self._landmarks.append(landmark)