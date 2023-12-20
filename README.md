# F1_Telemetry_VIProject

- Ruben Terceiro
- Daniel Ribeiro Cabral

# Prérequis 

Assurez-vous que les outils suivants sont installés sur votre ordinateur :

- Git : pour cloner le projet depuis GitHub.
- Docker : pour construire et exécuter le conteneur de l'application.
# Lancer le projet F1 - Telemetry

## Étape 1 : Cloner le Projet depuis GitHub

Ouvrez le terminal ou l'invite de commande et exécutez la commande suivante pour cloner le projet :
- `https://github.com/danielribeiroc/F1_Telemetry_VIProject.git`
- `cd F1_Telemetry_VIProject`

## Étape 2 : Vérifier le Dockerfile

Avant de construire l'image Docker, vérifiez que le **Dockerfile** existe à la racine du projet.
## Étape 3 : Build l'Image Docker
Toujours dans le terminal, exécutez la commande suivante pour construire l'image Docker :
- `docker build -t dashf1_app .`

## Étape 4 : Exécuter l'Application dans Docker
Après la construction de l'image, lancez l'application avec :

 - `docker run -h localhost -p 9002:9000 -d --name f1_app_container dashf1_app`

## Étape 5 : Accéder à l'Application Dash via le localhost

Ouvrez un navigateur web et allez à l'adresse **http://localhost:9002** Vous devriez voir l'application Dash en cours d'exécution.

## Description projet - Ma_VI_Master_Engineering - Data Science

**Public cible** : Fournir des indications sur les principales statistiques pour chaque course de F1 afin de pouvoir avoir une meilleure vue global du week-end.

**Source(s) de données:** : Librairie FastF1, [FastF1](https://github.com/theOehrly/Fast-F1)

**Descriptif du projet:** : Nous souhaitons proposer une visualisation pertinente pour le public de la F1 sur les résultats des derniers Grands Prix.  Pour cela nous allons avoir 4 onglets mis en place sur Dash et sous chacun nous aurons des graphiques qui font sens entre eux. Voici les visualisations mises en place ainsi que leurs objectifs :

**Onglet n°1**, Comparaison entre 2 pilotes :

- 1 : Graphique d’un circuit lors d’une certaine année illustrant les meilleurs temps par secteurs entre 2 pilotes.

- 2 : Overlaying speed traces of two laps, graphique line plot qui démontre de manière superposée les vitesses durant un tour entre 2 pilotes

**Interactivité** sur les variables du circuit, des 2 pilotes à comparer ainsi que de l’année de la course.

**Onglet n°2**, Vue globale d’un week-end de course :

- 1 : Qualifying Result Overview, différence de temps entre les pilotes durant la phase de qualification

- 2 : Position changes during a race

- 3 : Team Pace Comparaison, comparaison de la vitesse pour chaque écurie au travers des boîtes à moustaches

**Interactivité** sur les variables du circuit, ainsi que l’année de la course.

**Onglet n°3**, Classement général :

- 1 : Plot driver standings in a heatmap, classement des pilotes par courses

- 2 : Plot teams standings in a heatmap, classement des écuries par courses

**Interactivité** sur l’année du classement

**Lien du projet :** [Github Project](https://github.com/danielribeiroc/F1_Telemetry_VIProject)

**Date de présentation souhaitée :** Janvier 2024