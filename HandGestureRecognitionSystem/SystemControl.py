#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import time
import argparse
import itertools

import cv2 as cv
import numpy as np
import autopy
import mediapipe as mp
from pynput.keyboard import Key,Controller

from utils import CvFpsCalc
from model import KeyPointClassifier

from tkinter import *
from PIL import ImageTk, Image

root1 = None
cap = None


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args


def main(root, show_frame, testing_mode):
    global root1, cap
    root1 = Toplevel(root)
    root1.geometry("700x640")
    root1.configure(bg='black')

    if not show_frame:  # if user does not want to show the webcam frame
        root1.withdraw()

    lf1 = LabelFrame(root1, bg='red')
    lf1.pack()
    l1 = Label(lf1, bg='red')
    l1.pack()

    # Argument parsing
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    use_brect = True

    # Camera preparation
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    keyboard = Controller()
    is_caps = False

    frame_reduction = 150  # Frame Reduction
    smoothening = 7
    width_screen, height_screen = autopy.screen.size()
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    # MediaPipe model load
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    # call the classifier
    keypoint_classifier = KeyPointClassifier()

    # Read labels
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',
              encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    # FPS Measurement
    cvFpsCalc = CvFpsCalc(buffer_len=10)

    # start real-time video capture
    while True:
        fps = cvFpsCalc.get()

        # Camera capture
        ret, image = cap.read()
        time.sleep(0.05)
        if not ret:
            break
        image = cv.flip(image, 1)  # Mirror display
        debug_image = copy.deepcopy(image)

        # Detection implementation
        image = cv.cvtColor(debug_image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        # Get Hand Landmarks and Predict Gesture and Apply Functions
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # Bounding box calculation
                brect = calc_bounding_rect(image, hand_landmarks)
                # Landmark calculation
                landmark_list = calc_landmark_list(image, hand_landmarks)

                x1, y1 = landmark_list[8][0:]
                # x2, y2 = landmark_list[12][0:]
                cv.rectangle(image, (frame_reduction, frame_reduction),
                             (cap_width - frame_reduction - 300, cap_height - frame_reduction - 50), (255, 0, 255), 2)

                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(
                    landmark_list)

                # Hand sign classification
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

                # If it is not a testing mode
                if not testing_mode:
                    # Delay the execution time
                    if 0 <= hand_sign_id <= 34 or hand_sign_id == 39 or 41 <= hand_sign_id <= 46:
                        time.sleep(1.3)
                    elif hand_sign_id == 40:
                        time.sleep(0.6)
                    elif hand_sign_id == 36 or hand_sign_id == 37:
                        time.sleep(0.3)
                    # Functions Apply
                    if hand_sign_id == 0:
                        if is_caps:
                            keyboard.press("A")
                        else:
                            keyboard.press("a")

                    elif hand_sign_id == 1:
                        if is_caps:
                            keyboard.press("B")
                        else:
                            keyboard.press("b")

                    elif hand_sign_id == 2:
                        if is_caps:
                            keyboard.press("C")
                        else:
                            keyboard.press("c")

                    elif hand_sign_id == 3:
                        if is_caps:
                            keyboard.press("D")
                        else:
                            keyboard.press("d")

                    elif hand_sign_id == 4:
                        if is_caps:
                            keyboard.press("E")
                        else:
                            keyboard.press("e")

                    elif hand_sign_id == 5:
                        if is_caps:
                            keyboard.press("F")
                        else:
                            keyboard.press("f")

                    elif hand_sign_id == 6:
                        if is_caps:
                            keyboard.press("G")
                        else:
                            keyboard.press("g")

                    elif hand_sign_id == 7:
                        if is_caps:
                            keyboard.press("H")
                        else:
                            keyboard.press("h")

                    elif hand_sign_id == 8:
                        if is_caps:
                            keyboard.press("I")
                        else:
                            keyboard.press("i")

                    elif hand_sign_id == 9:
                        if is_caps:
                            keyboard.press("J")
                        else:
                            keyboard.press("j")

                    elif hand_sign_id == 10:
                        if is_caps:
                            keyboard.press("K")
                        else:
                            keyboard.press("k")

                    elif hand_sign_id == 11:
                        if is_caps:
                            keyboard.press("L")
                        else:
                            keyboard.press("l")

                    elif hand_sign_id == 12:
                        if is_caps:
                            keyboard.press("M")
                        else:
                            keyboard.press("m")

                    elif hand_sign_id == 13:
                        if is_caps:
                            keyboard.press("N")
                        else:
                            keyboard.press("n")

                    elif hand_sign_id == 14:
                        if is_caps:
                            keyboard.press("O")
                        else:
                            keyboard.press("o")

                    elif hand_sign_id == 15:
                        if is_caps:
                            keyboard.press("P")
                        else:
                            keyboard.press("p")

                    elif hand_sign_id == 16:
                        if is_caps:
                            keyboard.press("Q")
                        else:
                            keyboard.press("q")

                    elif hand_sign_id == 17:
                        if is_caps:
                            keyboard.press("R")
                        else:
                            keyboard.press("r")

                    elif hand_sign_id == 18:
                        if is_caps:
                            keyboard.press("S")
                        else:
                            keyboard.press("s")

                    elif hand_sign_id == 19:
                        if is_caps:
                            keyboard.press("T")
                        else:
                            keyboard.press("t")

                    elif hand_sign_id == 20:
                        if is_caps:
                            keyboard.press("U")
                        else:
                            keyboard.press("u")

                    elif hand_sign_id == 21:
                        if is_caps:
                            keyboard.press("V")
                        else:
                            keyboard.press("v")

                    elif hand_sign_id == 22:
                        if is_caps:
                            keyboard.press("W")
                        else:
                            keyboard.press("w")

                    elif hand_sign_id == 23:
                        if is_caps:
                            keyboard.press("X")
                        else:
                            keyboard.press("x")

                    elif hand_sign_id == 24:
                        if is_caps:
                            keyboard.press("Y")
                        else:
                            keyboard.press("y")

                    elif hand_sign_id == 25:
                        keyboard.press("0")

                    elif hand_sign_id == 26:
                        keyboard.press("1")

                    elif hand_sign_id == 27:
                        keyboard.press("2")

                    elif hand_sign_id == 28:
                        keyboard.press("3")

                    elif hand_sign_id == 29:
                        keyboard.press("4")

                    elif hand_sign_id == 30:
                        keyboard.press("5")

                    elif hand_sign_id == 31:
                        keyboard.press("6")

                    elif hand_sign_id == 32:
                        keyboard.press("7")

                    elif hand_sign_id == 33:
                        keyboard.press("8")

                    elif hand_sign_id == 34:
                        keyboard.press("9")

                    elif hand_sign_id == 35:
                        x3 = np.interp(x1, (frame_reduction, cap_width - frame_reduction - 300), (0, width_screen))
                        y3 = np.interp(y1, (frame_reduction, cap_height - frame_reduction - 50), (0, height_screen))

                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening

                        autopy.mouse.move(clocX, clocY)
                        plocX, plocY = clocX, clocY

                    elif hand_sign_id == 36:
                        autopy.mouse.click()

                    elif hand_sign_id == 37:
                        autopy.mouse.click(autopy.mouse.Button.RIGHT)

                    elif hand_sign_id == 38:
                        cv.putText(image, "stop", (10, 90),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                                   cv.LINE_AA)

                    elif hand_sign_id == 39:
                        keyboard.press(Key.space)

                    elif hand_sign_id == 40:
                        keyboard.press(Key.backspace)

                    elif hand_sign_id == 41:
                        keyboard.press(Key.enter)

                    elif hand_sign_id == 42:
                        keyboard.press(Key.up)

                    elif hand_sign_id == 43:
                        keyboard.press(Key.down)

                    elif hand_sign_id == 44:
                        keyboard.press(Key.right)

                    elif hand_sign_id == 45:
                        keyboard.press(Key.left)

                    elif hand_sign_id == 46:
                        if is_caps:
                            is_caps = False
                            keyboard.release(Key.caps_lock)
                        else:
                            is_caps = True
                            keyboard.press(Key.caps_lock)

                # Drawing part for the hand landmarks
                image = draw_bounding_rect(use_brect, image, brect)
                image = draw_landmarks(image, landmark_list)
                image = draw_info_text(
                    image,
                    brect,
                    handedness,
                    keypoint_classifier_labels[hand_sign_id]
                )

        image = draw_info(image, fps)

        # Screen reflection
        img = ImageTk.PhotoImage(Image.fromarray(image))
        l1['image'] = img

        root1.update()


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        # Thumb
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (255, 255, 255), 2)

        # Index finger
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (255, 255, 255), 2)

        # Middle finger
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (255, 255, 255), 2)

        # Ring finger
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (255, 255, 255), 2)

        # Little finger
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (255, 255, 255), 2)

        # Palm
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (255, 255, 255), 2)

    # Key Points
    for index, landmark in enumerate(landmark_point):
        if index == 0:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 1:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 2:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 3:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 4:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 5:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 6:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 7:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 8:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 9:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 10:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 11:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 12:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 13:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 14:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 15:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 16:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 17:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 18:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 19:
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 20:
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

    return image


def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # Outer rectangle
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 0, 0), 1)

    return image


def draw_info_text(image, brect, handedness, hand_sign_text):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                 (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text
    cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

    return image


def draw_info(image, fps):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
               1.0, (0, 0, 0), 4, cv.LINE_AA)
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
               1.0, (255, 255, 255), 2, cv.LINE_AA)
    return image


if __name__ == '__main__':
    main(root=Tk(), show_frame=True, testing_mode=False)
