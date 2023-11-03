# F1_Telemetry_VIProject

- Ruben Terceiro
- Daniel Ribeiro Cabral

## Description projet - Ma_VI_Master_Engineering - Data Science

**Public cible** : Fournir des indications sur les principales statistiques pour chaque course de F1 afin de pouvoir avoir une meilleure vue global du week-end.

**Source(s) de données:** : Librairie FastF1, [FastF1](https://github.com/theOehrly/Fast-F1)

**Descriptif du projet:** : Nous souhaitons proposer une visualisation pertinente pour le public de la F1 sur les résultats des derniers Grands Prix.  Pour cela nous allons avoir 4 onglets mis en place sur Dash et sous chacun nous aurons des graphiques qui font sens entre eux. Voici les visualisations mises en place ainsi que leurs objectifs :

**Onglet n°1**, Comparaison entre 2 pilotes :

-       1 : Graphique d’un circuit lors d’une certaine année illustrant les meilleurs temps par secteurs entre 2 pilotes.

-       2 : Overlaying speed traces of two laps, graphique line plot qui démontre de manière superposée les vitesses durant un tour entre 2 pilotes

**Interactivité** sur les variables du circuit, des 2 pilotes à comparer ainsi que de l’année de la course.

**Onglet n°2**, Vue globale d’un week-end de course :

-       1 : Qualifying Result Overview, différence de temps entre les pilotes durant la phase de qualification

-       2 : Position changes during a race

-       3 : Team Pace Comparaison, comparaison de la vitesse pour chaque écurie au travers des boîtes à moustaches

**Interactivité** sur les variables du circuit, ainsi que l’année de la course.

**Onglet n°3**, Classement général :

-       1 : Plot driver standings in a heatmap, classement des pilotes par courses

-       2 : Plot teams standings in a heatmap, classement des écuries par courses

**Interactivité** sur l’année du classement

**Lien du projet :** [Github Project](https://github.com/danielribeiroc/F1_Telemetry_VIProject)

**Date de présentation souhaitée :** Janvier 2024

## Mise en place de l'environnement conda
- Installez [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) ou [Anaconda](https://www.anaconda.com/) 
- Création d'un environnement conda pour ce projet : 
`conda create --name F1_Telemetry_VIProject python=3.8`
- Activez l'environnement Conda en utilisant la commande suivante (assurez-vous de le faire chaque fois que vous travaillez sur votre projet)
: `conda activate F1_Telemetry_VIProject`
- Installez les packages requis dans l'environnement Conda : ``pip install -r requirements.txt``
- Version de Python : 3.10

## Mise en place de l'environnement conda sur Pycharm

1. **Ouverture de Projet** : Ouvrez votre projet dans PyCharm.
2. **Accès aux Paramètres** : Allez dans File (Fichier) > Settings (Paramètres) sur Windows/Linux ou PyCharm > Preferences sur macOS.

3. **Sélection de l'Environnement Conda** : 
- Dans le panneau de gauche, allez à Project: **F1_Telemetry_VIProject > Python Interpreter**.
- Cliquez sur l'icône d'engrenage en haut à droite du panneau de l'interpréteur et sélectionnez **Add...** 
- Choisissez `Conda Environment`
- Sélectionnez `Existing environment` et parcourez le chemin de votre environnement Conda, généralement situé dans le répertoire Anaconda ou Miniconda.
- Sélectionnez le fichier `python` dans le répertoire de votre environnement Conda
- Cliquez sur `OK` pour fermer les fenêtres de configuration.