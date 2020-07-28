import time

import dlib
from Model.Utility import *


class FaceLandmarkDetector:
    def __init__(self, predictor_path):
        self._detector = dlib.get_frontal_face_detector()
        self._predictor = dlib.shape_predictor(predictor_path)

    def get_landmarks_frame_np(self, gray, rect):
        landmarks_frame = self._predictor(gray, rect)
        landmarks_frame = shape_to_np(landmarks_frame)
        return landmarks_frame

    def get_landmarks_normalized_from_frame(self, frame):
        new_frame = None
        new_landmarks_frame = None
        state = False
        #Detection delle facce su frame in scala di grigi
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self._detector(frame_gray,1)
        #Ciclo sulle facce per individuare i landmark non normalizati

        for (i, rect1) in enumerate(rects):
            landmarks = self.get_landmarks_frame_np(frame_gray, rect1)
            #Calcolo la matrice di rotazione da applicare al nuovo frame
            M = get_matrix_rotation_all(frame_gray, landmarks, 320)
            #Applico la matrice di rotazione al vecchio frame per ottenere l'invarianza
            new_frame = cv2.warpAffine(frame, M, (320, 320), flags=cv2.INTER_CUBIC)
            #Detection delle facce su frame in scala di grigi
            new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
            rects = self._detector(new_gray,1)
            #Ciclo sulle facce per individuare i landmark normalizzati
            for (x, y) in landmarks:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
            for (i, rect) in enumerate(rects):
                new_landmarks_frame = self.get_landmarks_frame_np(new_gray, rect)
                state = True
            (x, y, w, h) = rect_to_bb(rect1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame,new_frame, new_landmarks_frame, state
