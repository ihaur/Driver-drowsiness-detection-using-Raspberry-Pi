#!/bin/bash
# script pour lancer le projet sans réecrire à chaque fois ces commandes dans le terminal xD
cd /home/pi/drowsiness_detection_system/pi-drowsiness-detection
python3 pi_detect_drowsiness.py --cascade haarcascade_frontalface_default.xml --shape-predictor shape_predictor_68_face_landmarks.dat