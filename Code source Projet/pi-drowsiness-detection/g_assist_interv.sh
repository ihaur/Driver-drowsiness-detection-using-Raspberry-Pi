#!/bin/bash

#script qui fait appel à l'assistante google en donnant en entré des commandes vocales pré-enregistré dans le dossier commande vocale
cd /home/pi
source env/bin/activate

GA_SCRIPT_PATH="./assistant-sdk-python/google-assistant-sdk/googlesamples/assistant/grpc"
CMD_PATH="./commande_vocale"
DEVICE_ID=" --device-id votre_device_id --device-model-id votre__device__model__id "

cd ${GA_SCRIPT_PATH}


if [ $1 = "blague" ]
then
	python -m  pushtotalk ${DEVICE_ID} -i ${CMD_PATH}/joke.wav 
elif [ $1 = "devinette" ]
then
	python -m  pushtotalk ${DEVICE_ID} -i ${CMD_PATH}/devinette.wav
elif [ $1 = "citation" ]
then
	python -m  pushtotalk ${DEVICE_ID} -i ${CMD_PATH}/citation.wav
elif [ $1 = "call" ]
then
	python -m  pushtotalk ${DEVICE_ID} -i ${CMD_PATH}/call.wav #cette fonctionnalité doit être ajouté à l'aide de IFTTT
else
	python -m  pushtotalk ${DEVICE_ID} -i ${CMD_PATH}/tired.wav 
	python -m  pushtotalk ${DEVICE_ID} -i ${CMD_PATH}/stat_itin.wav  
fi
