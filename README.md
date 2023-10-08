# F1_Telemetry_VIProject

- Ruben Terceiro
- Daniel Ribeiro Cabral

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