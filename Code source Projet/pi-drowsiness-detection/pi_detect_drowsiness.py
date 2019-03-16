# USAGE
# python pi_detect_drowsiness.py --cascade haarcascade_frontalface_default.xml --shape-predictor shape_predictor_68_face_landmarks.dat
# Projet modifié à base du projet original : https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/
# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import picamera
import subprocess
import os
import random
import speech_recognition as sr
from gtts import gTTS
import urllib3

#*************************Fonctions pour la reconnaissance vocale *************************************#
def get_vocal_command():
        
        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:
                print("Say something !")
                audio = r.listen(source,None,2)

        try:
                t=r.recognize_google(audio, language='fr_FR')
                print ("You just said : " +t)
                return t
                      
        except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                say_something(u"Merci de répété votre demande")

        except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))


def say_something(msg):
        
        print("=>say_something() : " + msg)

        tts = gTTS(text=msg , lang='fr')
        tts.save("result.mp3")
        os.system("mpg123 result.mp3")

#*************************Fonctions pour tester la connexion internet **********************************#
def check_internet_on():
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.google.com')
        if (r.status == 200) :
                say_something("L'appareil est connecté")
        else:
                say_something("L'appareil n'est pas connecté à internet")
                


#*************************Fonctions de détection du EAR (eye aspect ratio)******************************#
        
def euclidean_dist(ptA, ptB):
        # compute and return the euclidean distance between the two
        # points
        return np.linalg.norm(ptA - ptB)

def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = euclidean_dist(eye[1], eye[5])
        B = euclidean_dist(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = euclidean_dist(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear

#########################################################################################################

# Vérifier la connexion internet
check_internet_on()
# Rappelez le conducteur de définir le numéro de téléphone de son ami dans l'app
say_something("N'oubliez pas de définir le numéro de ton ami à appeller sur l'application")
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
        help = "path to where the face cascade resides")
ap.add_argument("-p", "--shape-predictor", required=True,
        help="path to facial landmark predictor")
args = vars(ap.parse_args())



# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 8
# Declencher Google assistant après un certain nombre de détéction
G_assist = 0
# les choix de google assistant
G_choice = ['blague','devinette','citation']

# initialize the frame counter 
COUNTER = 0

# load OpenCV's Haar cascade for face detection (which is faster than
# dlib's built-in HOG detector, but less accurate), then create the
# facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = cv2.CascadeClassifier(args["cascade"])
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
# vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)

# loop over frames from the video stream
while True:
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                minNeighbors=5, minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE)

        # loop over the face detections
        for (x, y, w, h) in rects:
                # construct a dlib rectangle object from the Haar cascade
                # bounding box
                rect = dlib.rectangle(int(x), int(y), int(x + w),
                        int(y + h))

                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0

                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                # check to see if the eye aspect ratio is below the blink
                # threshold, and if so, increment the blink frame counter
                if ear < EYE_AR_THRESH:
                        COUNTER += 1

                        # if the eyes were closed for a sufficient number of
                        # frames, then sound the alarm
                        if COUNTER >= EYE_AR_CONSEC_FRAMES:
                                # draw an alarm on the frame
                                G_assist = G_assist + 1
                                print(G_assist)
                                #cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                #        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # otherwise, the eye aspect ratio is not below the blink
                # threshold, so reset the counter and alarm
                else:
                        COUNTER = 0

                # draw the computed eye aspect ratio on the frame to help
                # with debugging and setting the correct eye aspect ratio
                # thresholds and frame counters
                cv2.putText(frame, "EAR: {:.3f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                #choix aléatoire de lancer une blague, une devinette ou une citation
                choix_google = random.choice(G_choice)

                if ( ((G_assist%4)==0) and (G_assist>0) and (G_assist< 9)):
                        # Lancement d'un bash "./g_assist_interv.sh" avec l'argument "choix_google": appel de l'assistant google pour lancer une blague, une devinette ou une citation
                        cv2.putText(frame, "FATIGUE ALERT!", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        os.system("./g_assist_interv.sh %s" % str(choix_google))
                        print("tired")
                        G_assist = G_assist + 1
                #initialisation de reponse
                reponse = None        
                if (G_assist >= 9):
                        #Lancement d'un bash "./g_assist_interv.sh" sans argument : appel de l'assistant google pour lancer un message vocale et indiquer l'aire de repos le plus proche
                        cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        os.system("./g_assist_interv.sh")
                        say_something("Voulez vous que j'appelle un ami ?")
                        while(reponse == None):        
                                reponse = get_vocal_command()
                                print(reponse)
                        if reponse == "ok" :
                        	#Lancement d'un bash "./g_assist_interv.sh" avec l'argument "call" : appel de l'assistant google pour lancer une notification au tel pour que ce dernier lance un appel
                                os.system("./g_assist_interv.sh call")
                        else:
                                say_something("D'accord comme vous voulez")
                        print("sleepy")
                        G_assist = 0
                
        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
 
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
