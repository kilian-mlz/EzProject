Avant de pouvoir lancer le projet, veillez a avoir Docker installé sur votre machine puis veuillez lancer le fichier "docker-compose.yml" afin d'initialiser une bdd dans un container mariadb sur docker (Mot de passe root = admin).

Lancer également le fichier create.py afin de crée les tables dans la base de données (à ne lancer qu'une seule fois !).

Ensuite, lancer les fichiers : - "user_api.py"
			       - "board_api.py"
			       - "notification_api.py"

Puis pour finir, lancer le fichier "client.py".