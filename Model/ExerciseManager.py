import os
from pathlib import Path

import cv2
import numpy as np
from Model.FaceLandmarkDetector import FaceLandmarkDetector
from Model.MetricLearner import MetricLearner
from Model.VideoFE import VideoFE
from dtw import *

def generate_landmark_array(path):
    all_landmarks = []
    for file in os.listdir(path):
        if file.endswith(".npy"):
            path_file_lanmark = os.path.join(path, file)
            all_landmarks.append(np.load(path_file_lanmark, allow_pickle=True))
    return np.array(all_landmarks)

class ExerciseManager:
    def __init__(self, type, name):
        self._videos_correct = []
        self._videos_bad = []
        for file in os.listdir("Exercises"+'\\'+type+'\\'+name+'\\'+"Correct"):
            if file.endswith(".mp4"):
                self._videos_correct.append(file)
        for file in os.listdir("Exercises" + '\\' + type + '\\' + name + '\\' + "Bad"):
            if file.endswith(".mp4"):
                self._videos_bad.append(file)
        self._landmarks_correct = generate_landmark_array("Exercises" + '\\' + type + '\\' + name + '\\' + "Correct")
        self._landmarks_bad = generate_landmark_array("Exercises" + '\\' + type + '\\' + name + '\\' + "Bad")
        self._landmarks_correct_trainig = generate_landmark_array("Exercises" + '\\' + type + '\\' + name + '\\' + "Correct\\Training")
        self._landmarks_bad_training = generate_landmark_array("Exercises" + '\\' + type + '\\' + name + '\\' + "Bad\\Training")
        self._type=type
        self._name=name
        self._face_detector = FaceLandmarkDetector('Model/shape_predictor_68_face_landmarks.dat')

        self._description = self.load_description()

    def get_landmarks(self):
        return self._landmarks_correct, self._landmarks_bad, self._landmarks_correct_trainig, self._landmarks_bad_training

    def get_bad_videos(self):
        return self._videos_bad

    def get_correct_videos(self):
        return self._videos_correct

    def get_description(self):
        return self._description

    def replace_description(self, new_description):
        file = open("Exercises" + "\\" + self._type + "\\" + self._name + "\\" + "Description.txt", "r+")
        file.write(new_description)
        self._description = new_description

    def insert_new_video(self, type_video):
        if type_video == "Bad":
            name_video = str(len(self._videos_bad))
        else:
            name_video = str(len(self._videos_correct))

        new_video = VideoFE(name_video)
        path = "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + str(type_video) + "\\" + new_video.get_name()
        face_detector = FaceLandmarkDetector('Model/shape_predictor_68_face_landmarks.dat')
        cap = cv2.VideoCapture(0)
        if not(cap.isOpened()):
            print("Impossibile avviare la camera, controllare che sia accesa!")
            return 0
        count = 0
        count2 = -1
        percentage1 = 0
        percentage2 = 0
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter( path + ".mp4", fourcc, 10.00, (640, 480))
        landmarks_zero = None



        while cap.isOpened():
            rval, frame = cap.read()
            # frame = imutils.resize(frame, width=680)
            if rval == False:
                break

            output = np.zeros((630, 1380, 3), dtype="uint8")
            output[75:555, 370:1010] = frame

            cv2.rectangle(output, (370,580), (1010,605), (0, 0, 255), -1)

            frame_dot, frame_normalized, landmarks_normalized, control = face_detector.get_landmarks_normalized_from_frame(frame)
            if(control):
                output[155:475, 25:345] = frame_normalized
                output[75:555, 370:1010] = frame_dot
                for (x, y) in landmarks_normalized:
                    cv2.circle(frame_normalized, (x, y), 1, (0, 0, 255), -1)
                frame_landmrks_normalized = np.zeros((320,320,3), dtype="uint8")
                for (x, y) in landmarks_normalized:
                    cv2.circle(frame_landmrks_normalized, (x, y), 1, (0, 0, 255), -1)

                output[155:475, 1035:1355] = frame_landmrks_normalized
                if count == 37 or count2 >=0:
                    out.write(frame)
                    if count == 37:
                        cv2.imwrite("Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + str(type_video) + "\\Training\\temp_init.png", frame)
                        landmarks_zero = landmarks_normalized
                    landmarks_delta = landmarks_normalized - landmarks_zero
                    new_video.insert_landmark(landmarks_delta)
                percentage1 = (100 / 40) * count
                if (percentage1 <= 100):
                    cv2.rectangle(output, (370, 580), (370 + int(percentage1 * 6.4), 605), (0, 255, 255), -1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = "Preparati mantenendo una POSIZIONE DI RIPOSO."

                    textsize = cv2.getTextSize(text, font, 1, 2)[0]
                    # get center coord text
                    textX = int((textsize[0]) / 2)
                    textY = int((textsize[1]) / 2)

                    cv2.putText(output, text, (690 - textX, 37 + textY), font, 1, (255, 255, 255), 2)
                    percentage1 = (100 / 40) * count
                    count += 1
                    count2 = -1
                else:
                    cv2.rectangle(output, (370, 580), (1010, 605), (0, 255, 255), -1)

                    percentage2 = (100 / 39) * (count2+1)

                    if (percentage2 < 100):
                        cv2.rectangle(output, (370, 580), (370 + int(percentage2 * 6.4), 605), (0, 255, 0), -1)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        text = "Esegui l'esercizio mantenendo la smorfia fino al termine"

                        count2 += 1
                        textsize = cv2.getTextSize(text, font, 1, 2)[0]
                        # get center coord text
                        textX = int((textsize[0]) / 2)
                        textY = int((textsize[1]) / 2)

                        cv2.putText(output, text, (690 - textX, 37 + textY), font, 1, (255, 255, 255), 2)
                    else:
                        cv2.rectangle(output, (370, 580), (1010, 605), (0, 255, 0), -1)
            else:
                if (percentage1 <= 100):
                    cv2.rectangle(output, (370, 580), (370 + int(percentage1 * 6.4), 605), (0, 255, 255), -1)
                else:
                    cv2.rectangle(output, (370, 580), (370 + int(percentage2 * 6.4), 605), (0, 255, 255), -1)

            cv2.imshow("Nuovo Video", output)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # If q is pressed then exit
                break
            if len(new_video.get_landmarks()) == 39:
                cv2.imwrite("Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + str(type_video) + "\\Training\\temp_fin.png", frame)
                np.save("Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + str(type_video) + "\\Training\\temp_fin.npy", new_video.get_landmarks()[38])

            if len(new_video.get_landmarks()) == 40:
                np.save(path + ".npy", new_video.get_landmarks())
                if type_video == 0:
                    self._videos_bad.append(new_video)
                else:
                    self._videos_correct.append(new_video)
                break

        cap.release()
        cv2.destroyAllWindows()


    def remove_video(self, type_video, name_video):
        path = "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + type_video + "\\" + name_video
        os.remove(path + ".mp4")
        os.remove(path + ".npy")
        if(type_video == "Correct"):
            self._videos_correct = []
            i = 0
            for file in sorted(os.listdir("Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Correct"), key = len):
                if file.endswith(".mp4"):
                    if(True):
                        os.rename("Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Correct" + "\\" + file[:-4] + ".mp4", "Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Correct" + "\\" + str(i) + ".mp4")
                        os.rename("Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Correct" + "\\" + file[:-4] + ".npy", "Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Correct" + "\\" + str(i) + ".npy")
                        self._videos_correct.append(i)
                    else:
                        self._videos_correct.append(i)
                    i = i + 1
        else:
            self._videos_bad = []
            i = 0
            for file in sorted(os.listdir("Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Bad"), key = len):
                if file.endswith(".mp4"):
                    if (True):
                        os.rename("Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Bad" + "\\" + file[:-4] + ".mp4",
                                  "Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Bad" + "\\" + str(i) + ".mp4")
                        os.rename("Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Bad" + "\\" + file[:-4] + ".npy",
                                  "Exercises" + '\\' + self._type + '\\' + self._name + '\\' + "Bad" + "\\" + str(i) + ".npy")
                        self._videos_bad.append(i)
                    else:
                        self._videos_bad.append(i)
                    i = i + 1

    def load_description(self):
        path = "Exercises" + "\\" +  self._type + "\\" + self._name + "\\" + "Description.txt"
        file = open(path, "r")
        self._description = file.read()
        file.close()
        return self._description

    def execute_exercise(self):
        new_video = VideoFE("nuovo_video")
        face_detector = FaceLandmarkDetector('Model/shape_predictor_68_face_landmarks.dat')
        cap = cv2.VideoCapture(0)

        count = 0
        count2 = -1
        percentage1 = 0
        percentage2 = 0

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter("Exercises/temp.mp4", fourcc, 10.00, (640, 480))
        landmarks_zero = None
        if not(cap.isOpened()):
            print("Impossibile avviare la camera, controllare che sia accesa!")
            return 0

        while cap.isOpened():
            rval, frame = cap.read()
            #frame = imutils.resize(frame, width=680)
            if rval == False:
                break
            frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
            output = np.zeros((630, 1380, 3), dtype="uint8")
            output[75:555, 370:1010] = frame

            cv2.rectangle(output, (370,580), (1010,605), (0, 0, 255), -1)

            #cv2.imshow("FaceLandmarksGray", frame)
            frame_dot, frame_normalized, landmarks_normalized, control = face_detector.get_landmarks_normalized_from_frame(frame)
            if(control):
                output[155:475, 25:345] = frame_normalized
                output[75:555, 370:1010] = frame_dot
                for (x, y) in landmarks_normalized:
                    cv2.circle(frame_normalized, (x, y), 1, (0, 0, 255), -1)
                frame_landmrks_normalized = np.zeros((320, 320, 3), dtype="uint8")
                for (x, y) in landmarks_normalized:
                    cv2.circle(frame_landmrks_normalized, (x, y), 1, (0, 0, 255), -1)

                output[155:475, 1035:1355] = frame_landmrks_normalized
                if count == 37 or count2 >= 0:
                    out.write(frame)
                    if count == 37:
                        cv2.imwrite("Exercises\\temp_init.png", frame)
                        landmarks_zero = landmarks_normalized
                    landmarks_delta = landmarks_normalized - landmarks_zero
                    new_video.insert_landmark(landmarks_delta)

                percentage1 = (100 / 40) * count
                if (percentage1 <= 100):
                    cv2.rectangle(output, (370, 580), (370 + int(percentage1 * 6.4), 605), (0, 255, 255), -1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = "Preparati mantenendo una POSIZIONE DI RIPOSO."

                    textsize = cv2.getTextSize(text, font, 1, 2)[0]
                    # get center coord text
                    textX = int((textsize[0]) / 2)
                    textY = int((textsize[1]) / 2)

                    cv2.putText(output, text, (690 - textX, 37 + textY), font, 1, (255, 255, 255), 2)
                    percentage1 = (100 / 40) * count
                    count += 1
                    count2 = -1
                else:
                    cv2.rectangle(output, (370, 580), (1010, 605), (0, 255, 255), -1)

                    percentage2 = (100 / 39) * (count2+1)

                    if (percentage2 < 100):
                        cv2.rectangle(output, (370, 580), (370 + int(percentage2 * 6.4), 605), (0, 255, 0), -1)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        text = "Esegui l'esercizio mantenendo la smorfia fino al termine"

                        textsize = cv2.getTextSize(text, font, 1, 2)[0]
                        # get center coord text
                        textX = int((textsize[0]) / 2)
                        textY = int((textsize[1]) / 2)

                        cv2.putText(output, text, (690 - textX, 37 + textY), font, 1, (255, 255, 255), 2)
                        count2 += 1

                    else:
                        cv2.rectangle(output, (370, 580), (1010, 605), (0, 255, 0), -1)
            else:
                if (percentage1 <= 100):
                    cv2.rectangle(output, (370, 580), (370 + int(percentage1 * 6.4), 605), (0, 255, 255), -1)
                else:
                    cv2.rectangle(output, (370, 580), (370 + int(percentage2 * 6.4), 605), (0, 255, 255), -1)

            cv2.imshow("Esegui Esercizio", output)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # If q is pressed then exit
                break

            if len(new_video.get_landmarks()) == 39:
                cv2.imwrite("Exercises\\temp_fin.png", frame)
                np.save("Exercises\\temp_fin.npy", new_video.get_landmarks()[38])

            if len(new_video.get_landmarks()) == 40:
                np.save("Exercises/temp.npy", new_video.get_landmarks())
                break
        id_correct = ""
        id_bad = ""

        metricLearner = MetricLearner()
        metricLearner.load_learner("Exercises"+'\\'+self._type+'\\'+self._name+'\\')
        metric = metricLearner.get_learner().get_metric()
        min_correct =  np.math.inf
        for file in os.listdir("Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Correct"):
            if file.endswith(".npy"):
                landmark_correct = np.load("Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Correct\\" + file, allow_pickle=True)
                landmark_esercizio = np.array(new_video.get_landmarks())
                alignement = dtw(landmark_correct.reshape(40,68*2),landmark_esercizio.reshape(40,68*2),metric)
                if(alignement[0]<min_correct):
                    min_correct = alignement[0]
                    id_correct = self._type+'\\'+self._name+'\\' + "Correct\\" + file[:-3] + "mp4"
        min_bad =  np.math.inf
        for file in os.listdir("Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Bad"):
            if file.endswith(".npy"):
                landmark_bad = np.load("Exercises"+'\\'+self._type+'\\'+self._name+'\\' + "Bad\\" + file, allow_pickle=True)
                landmark_esercizio = np.array(new_video.get_landmarks())
                alignement = dtw(landmark_bad.reshape(40,68*2),landmark_esercizio.reshape(40,68*2),metric)
                if (alignement[0]< min_bad):
                    min_bad =alignement[0]
                    id_bad = self._type+'\\'+self._name+'\\' + "Bad\\" + file[:-3] + "mp4"

        cap.release()
        cv2.destroyAllWindows()

        if(min_correct < min_bad):
            return 1, id_bad, id_correct, str(min_bad), str(min_correct)
        else:
            return 0, id_bad, id_correct, str(min_bad), str(min_correct)

