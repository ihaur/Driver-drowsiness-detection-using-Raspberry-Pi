# Driver-drowsiness-detection-using-Raspberry-Pi

La fatigue est un facteur important de cause d’accidents mortels, notamment sur voie rapide. Dans sa globalité, la fatigue joue un rôle dans environ 10% des accidents mortels.

Au volant, la fatigue se traduit par une attention moins forte, un temps de réaction plus long et une analyse des situations beaucoup plus longue. De fait, la prise de décision face à un danger est beaucoup moins évidente, multipliant les risques d’accident. Dans le pire des cas, la fatigue conduit à la somnolence avec un risque d’accident.

La fatique est souvent minimisée par les conducteur, pourtant les conséquences sont comparables à celles de la conduite sous influence de l’alcool :  

** Difficulté à maintenir sa trajectoire  
** Temps de réaction plus long  
** Micro-sommeils  
** Baisse de l’attention
** Difficulté à maintenir une vitesse constante

Les principales causes de la fatique se présentent comme suit : 

** Déficit de sommeil : Tout le monde peut être confronté à un déficit de sommeil, dont les causes peuvent être multiples. Le problème est qu’un déficit de sommeil ne se résorbe pas facilement et la seule manière de le combler est de dormir. S’il est difficile de quantifier le nombre d’heures de sommeil idéal pour l’individu moyen, nous savons que certaines catégories de conducteur sont d’avantage exposés aux risques de déficit de sommeil: chauffeurs routiers , livreurs, personnes travaillant avec des horaires décalés... 

** Horloge biologique : Nous avons tous une horloge biologique qui implique des périodes d’éveil et de fatigue en fonction du moment de la journée. Ainsi l’analyse des accidents dus à une baisse de vigilance montre qu’il y a deux pics d’accidents. Le premier se situe entre 13 et 15 h, et le deuxième ,beaucoup plus important, se situe aux alentours de 2h du matin.   

** Médicaments alcool drogues : Outre l’alcool et les drogues, beaucoup de médicaments ont également un effet important sur l’état d’éveil de l’usager. Alors que les psychotropes sont bien connus comme pouvant altérer l’état d’éveil, d’autres médicaments plus ordinaires, comme les antiallergiques et remèdes contre le rhume, peuvent avoir un effet similaire.

** Conditions de circulation : Les conditions de circulation peuvent avoir une grande influence sur l’état de vigilance du conducteur. Un trajet long et monotone induit un risque plus élevé de baisse de vigilance.

Les signes précurseurs de fatigue peuvent être repérées à temps par le conducteur via les signes précurseurs suivants : 

** Difficulté à maintenir la tête droite  

** Bâillements à répétition 

** Lourdeur des paupières et picotement des yeux
  
** Difficultés à maintenir une vitesse constante 
 
** Troubles de la concentration 

** Pensées décousues  

** Augmentation des gestes « autocentrés3 »

Dans le but de garantir la sécurité routière pour les usagers de la route comprennent les automobilistes, les conducteurs des transports publics routiers (principalement les autobus et autocars), nous avons développé ce système de détection de fatigue en se basant sur la lourdeur des paupières et picotement des yeux. 

L'objectif de notre projet alors est de détecter le mouvement des yeux, et conseiller au conducteur de faire une pause avant qu’il ne soit trop tard. Les informations nécessaires à cette alerte sont fournies par le traitement d'image sur la Raspberry Pi.  

Ce système de sécurité vise à réduire le nombre d'accidents et prendre conscience des risques. 

Les trois axes Problème/Public/Valeur sont les suivants :  

**Problème :    Sécurité routière et accident                         

**Public   :    Les usagers de la route comprennent les automobilistes, les conducteurs des transports publics routiers (autobus et autocars)

**Valeur   :    Réduire le nombre d'accidents et prendre conscience des risques. 

Nous avons exploré le problème de la sécurité routière et accident avec un questionnaire descriptif aux usagers de la route, le lien du formulaire est le suivant : 

https://docs.google.com/forms/d/e/1FAIpQLSfq_Wrobv6VXVaXn0eOo6nLWVVZ279OHCWfPg3CBnX3iYEJzg/viewform?vc=0&c=0&w=1

Nous définissons les entrées / sorties de notre système comme suit :

** Entrée : Mouvement des yeux

** Sortie : Voix personnalisées en utilisant l'assistante Google
                        
La première étape consiste à se connceter en SSH et VNC sur le Raspberry-Pi. Pour cela, nous avons récupéré l'adresse IP de la carte en se connectant à un point d'accès Wi-Fi configuré sur la carte SDK. Le lien suivant décrit les étapes suivis pour accéder à la Raspberry-Pi par SSH et VNC : https://www.windtopik.fr/ssh-vnc-raspberrypi/ .

Une fois connecté sur VNC, nous avons suivi les étapes du lien ci-dessous pour installer l'assistante Google sur la Raspberry Pi : https://developers.google.com/assistant/sdk/guides/library/python/embed/setup. 

Nous avons également installé OpenCV sur la raspberry en suivant les étapes du lien suivant : https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.deciphertechnic.com%2Finstall-opencv-python-on-raspberry-pi%2F%3Ffbclid%3DIwAR1CpzMVfxFXZObqhYzde5jQN5CINdQEMsLCjzKxA1sw0A36cDftsUu2MA0&h=AT3yyFiD_V991j70nm2bqHsZgHdpt309LN6ucBCxh-Zdhy9Ig0r5Gu0y57kDzyYpvglPr_TbSNAaEzi1ZS7wO1o4qatrRIkc2ale2bIX4dmI_h-oSZnksCc3z_5OGB7jIVDJcQ


 
