# Driver-drowsiness-detection-using-Raspberry-Pi

La fatigue est un facteur important de cause d’accidents mortels, notamment sur voie rapide. Dans sa globalité, la fatigue joue un rôle dans environ 10% des accidents mortels.

Au volant, la fatigue se traduit par une attention moins forte, un temps de réaction plus long et une analyse des situations beaucoup plus longue. De fait, la prise de décision face à un danger est beaucoup moins évidente, multipliant les risques d’accident. Dans le pire des cas, la fatigue conduit à la somnolence avec un risque d’accident.

Dans le but de garantir la sécurité routière pour les usagers de la route comprennent les automobilistes, les conducteurs des transports publics routiers (principalement les autobus et autocars), nous avons développé ce système de détection de fatigue. 

L'objectif de notre projet est de détecter le mouvement des yeux, et conseiller au conducteur de faire une pause avant qu’il ne soit trop tard. Les informations nécessaires à cette alerte sont fournies par le traitement d'image sur la Raspberry Pi.  

Ce système de sécurité vise à réduire le nombre d'accidents et prendre conscience des risques. 

Les trois axes Problème/Public/Valeur sont les suivants :  

**Problème :    Sécurité routière et accident                         

**Public   :    Les usagers de la route comprennent les automobilistes, les conducteurs des transports publics routiers (autobus et autocars)

**Valeur   :    Réduire le nombre d'accidents et prendre conscience des risques. 

Nous définissons les entrées / sorties de notre système comme suit : 
            * Entrée : Mouvement des yeux
            * Sortie : Voix personnalisées en utilisant l'assistante Google
                        
La première étape consiste à se connceter en SSH et VNC sur le Raspberry-Pi. Pour cela, nous avons récupéré l'adresse IP de la carte en se connectant à un point d'accès Wi-Fi configuré sur la carte SDK. Le lien suivant décrit les étapes suivis pour accéder à la Raspberry-Pi par SSH et VNC : https://www.windtopik.fr/ssh-vnc-raspberrypi/ .

Une fois connecté sur VNC, nous avons suivi les étapes du lien ci-dessous pour installer l'assistante Google sur la Raspberry Pi : https://developers.google.com/assistant/sdk/guides/library/python/embed/setup. 



 
