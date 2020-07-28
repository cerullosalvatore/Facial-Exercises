import cv2
import numpy as np


def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    # ritorna una tupla (x, y, w, h)
    return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
    # inizializza l'elenco di coordinate (x, y)
    coords = np.zeros((68, 2), dtype=dtype)

    # esegue un loop sui 68 landmarks del viso e li converte in tuple 2d di coordinate (x, y)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
     # ritorna la lista delle coordinate (x,y)
    return coords

def get_matrix_rotation_all(self, landmarks, image_size_output):
    # extract the left and right eye (x, y)-coordinates
    # estraggo le coordinate degli occhi in base ai valori calcolati precedentemente
    sx_occhio_coords = landmarks[42:48]
    dx_occhio_coords = landmarks[36:42]

    # calcolo il centro degli occhi
    sx_occhio_center = sx_occhio_coords.mean(axis=0).astype("int")
    dx_occhio_center = dx_occhio_coords.mean(axis=0).astype("int")

    # calcolo l'angolo tra i centri degli occhi definendo la rotazione da applicare per normalizzarla
    dX = dx_occhio_center[0] - sx_occhio_center[0]
    dY = dx_occhio_center[1] - sx_occhio_center[1]
    angle = np.degrees(np.arctan2(dY, dX)) - 180
    #capture y rotation
    # compute center (x, y)-coordinates (i.e., the median point)
    # between the two eyes in the input image
    eyesCenter = ((sx_occhio_center[0] + dx_occhio_center[0]) // 2,(sx_occhio_center[1] + dx_occhio_center[1]) // 2)
    # calcolo la scala
    dist_real = np.sqrt((dX ** 2) + (dY ** 2))

    dist_ideal = image_size_output * 0.21
    scala = dist_ideal / dist_real
    # grab the rotation matrix for rotating and scaling the face
    M = cv2.getRotationMatrix2D(eyesCenter, angle, scala)

    # applico la traslazione
    M[0, 2] += (image_size_output / 2) - eyesCenter[0]
    M[1, 2] += (image_size_output / 2) - eyesCenter[1]

    return M
