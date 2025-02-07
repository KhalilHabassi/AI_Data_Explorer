# AI Data Explorer

AI Data Explorer est une application web interactive qui permet d'explorer, analyser et visualiser des données tabulaires grâce à l'intelligence artificielle. Elle intègre une interface utilisateur conviviale avec Streamlit, le traitement et l'analyse de données avec Pandas, ainsi que la génération de résumés et de visualisations via l'API de Claude (Anthropic).

## Fonctionnalités

- **Chargement et traitement des données**  
  - Supporte les formats CSV, Excel et Parquet.
  - Nettoyage automatique des données (suppression de colonnes vides, conversion de types, traitement des valeurs manquantes).
  - Échantillonnage pour limiter le volume de données.

- **Génération d'insights et de visualisations**  
  - Utilise l'API de Claude pour générer des résumés statistiques, des interprétations et des suggestions de visualisations.
  - Génère dynamiquement du code de visualisation à exécuter directement via Streamlit.
  - Offre des visualisations interactives (histogrammes, scatter plots, heatmaps, etc.) avec Plotly.

- **Interface utilisateur interactive**  
  - Tableau de bord organisé en plusieurs onglets (description du dataset, visualisation générale, visuels dynamiques, historique des requêtes).
  - Personnalisation du thème et rechargement des visualisations existantes.

## Installation

### Prérequis


- **Poetry**  
- **python = "^3.11"**  
- **treamlit = "^1.33.0"**  
- **pandas = "^2.2.0"**  
- **plotly = "^5.18.0"**  
- **seaborn = "^0.13.2"**  
- **python-dotenv = "^1.0.0"**  
- **requests = "^2.31.0"**  
- **openai = "^1.12.0"**  
- **numpy = "^1.26.0"**  
- **scipy = "^1.12.0"**  
- **boto3 = "^1.34.0"**  
- **anthropic = "^0.45.2"**  

### Configuration de l'environnement

1. **Cloner le dépôt :**

Commencez par récupérer le projet depuis GitHub :

git clone https://github.com/KhalilHabassi/AI_Data_Explorer.git

2. **Installer les dépendances avec Poetry :**
Utilisez Poetry pour gérer les dépendances et assurer un environnement stable :
poetry install

3.  **Configuration optionnelle :**
 
Le fichier settings.toml contient plusieurs paramètres de configuration (limite de lignes, thème, nombre maximal de tokens, etc.).
Vous pouvez le modifier en fonction de vos besoins.

4.  **Exécution de l'application :**

Pour démarrer l'application en mode développement avec Streamlit, utilisez la commande suivante :

poetry run streamlit run app.py


Une fois lancée, ouvrez le lien généré dans votre navigateur pour accéder à l'interface.

### Choix Techniques:

✅ Interface utilisateur
Streamlit : Création rapide et interactive d’interfaces web.

✅ Génération de contenu via IA
Anthropic Claude : Génération de résumés, interprétations et code de visualisation via la classe ClaudeClient.

✅ Configuration et gestion des secrets
python-dotenv : Chargement des variables d’environnement depuis .env.
configparser : Lecture des paramètres depuis settings.toml.

✅ Gestion du projet
Poetry : Gestion des dépendances et création d'environnements virtuels reproductibles.


### Structure du Projet

📂 app.py
Point d’entrée de l’application.
Interface utilisateur avec Streamlit (gestion des interactions, affichage des visualisations, historique des requêtes).

📂 api.py
Communication avec l’API Claude (Anthropic) via la classe ClaudeClient.

📂 config.py
Chargement des configurations depuis settings.toml et des variables d’environnement stockées dans .env.

📂 data_loader.py
Chargement des jeux de données (CSV, Excel, Parquet).
Échantillonnage des données pour optimiser les performances.

📂 dataprocessor.py
Nettoyage et transformation des données.
Suppression des colonnes vides, conversion des types, gestion des valeurs manquantes.
Génération d’un résumé statistique des datasets.

📂 .env
Fichier contenant les informations sensibles (ex. : clé API).

📂 settings.toml
Fichier centralisé de configuration :
Paramètres de traitement des données.
Options de visualisation.
Gestion des interactions avec l’API.

📂 pyproject.toml & poetry.lock
Fichiers de configuration de Poetry pour assurer une gestion stable et reproductible des dépendances.
