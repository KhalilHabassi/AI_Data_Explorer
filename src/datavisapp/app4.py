import json
import streamlit as st
import pandas as pd
from datavisapp.data_loader import DataLoader
from datavisapp.data_processor import DataProcessor
from datavisapp.api import ClaudeClient
from datavisapp.config import settings

##############################
# Fonction pour déduire le logo selon le thème
def get_logo_url(custom_theme):
    theme_lower = custom_theme.lower()
    if "musique" in theme_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
    elif "restaurant" in theme_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Spaghetti_al_Pomodoro_%28cropped%29.jpg/640px-Spaghetti_al_Pomodoro_%28cropped%29.jpg"
    else:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Project_chart_bar.svg/640px-Crystal_Project_chart_bar.svg.png"

##############################
def main():
    st.set_page_config(
        page_title="AI Data Explorer",
        layout="wide",
        page_icon=":bar_chart:",
        initial_sidebar_state="expanded"
    )
    
    # Initialisation des variables de session
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'dataset_summary' not in st.session_state:
        st.session_state.dataset_summary = None
    if 'visualization_code' not in st.session_state:
        st.session_state.visualization_code = None
    if 'insights' not in st.session_state:
        st.session_state.insights = None
    if 'history' not in st.session_state:
        st.session_state.history = []  # Historique des requêtes
    if 'viz_type' not in st.session_state:
        st.session_state.viz_type = "Histogramme"  # Type de visuel par défaut
    if 'theme_choice' not in st.session_state:
        st.session_state.theme_choice = "Standard"  # Thème par défaut
    if 'dynamic_visualization_code' not in st.session_state:
        st.session_state.dynamic_visualization_code = None

    # Barre latérale : Chargement du dataset et choix du type de graphique général
    with st.sidebar:
        st.header("Configuration")
        uploaded_file = st.file_uploader("Charger un dataset", type=['csv', 'xlsx'])
        
        st.subheader("Type de visualisation général")
        st.session_state.viz_type = st.selectbox(
            "Choisir le type de graphique",
            options=[
                "Histogramme", 
                "Toile d'araignée", 
                "Matrice de corrélation", 
                "Scatter", 
                "Heatmap", 
                "Choropleth", 
                "Interactif dynamique"
            ],
            index=0
        )
        if uploaded_file:
            with st.spinner("Chargement et traitement du dataset..."):
                process_data(uploaded_file)
                if st.session_state.processed_data and not st.session_state.dataset_summary:
                    generate_dataset_summary()

    # Partie principale : Titre, choix du thème personnalisé et saisie de la question générale
    st.title("AI Data Explorer")
    st.write("### Explorez et visualisez vos données tabulaires grâce à l'IA")
    
    st.subheader("Entrez votre thème (texte libre)")
    st.session_state.theme_choice = st.text_input("Thème de l'interface :", value="Standard")
    logo_url = get_logo_url(st.session_state.theme_choice)
    st.image(logo_url, width=200)
    
    user_query = st.text_area("Posez votre question pour la visualisation générale :")
    
    if st.session_state.processed_data and user_query:
        with st.spinner("Génération de la visualisation..."):
            generate_visualization(user_query, st.session_state.viz_type)
            st.session_state.history.append({
                "query": user_query,
                "interpretation": st.session_state.insights.get("interpretation"),
                "visualization_code": st.session_state.visualization_code,
                "viz_type": st.session_state.viz_type,
                "theme": st.session_state.theme_choice,
                "type": "Générale"
            })

    # Organisation de l'interface principale en onglets (ajout du 4ème onglet)
    tabs = st.tabs(["Description du Dataset", "Visualisation Générale", "Visuels Dynamiques", "Historique des Requêtes"])
    
    with tabs[0]:
        st.write("## Variables du dataset")
        if st.session_state.processed_data:
            variables = pd.DataFrame({
                "Index": range(1, len(st.session_state.processed_data['df'].columns) + 1),
                "Nom de variable": st.session_state.processed_data['df'].columns
            })
            st.table(variables)
        if st.session_state.dataset_summary:
            st.write("## Résumé du dataset")
            st.markdown(st.session_state.dataset_summary)
    
    with tabs[1]:
        if st.session_state.visualization_code:
            display_dashboard()
        else:
            st.info("Aucune visualisation générée pour le moment.")
    
    # Onglet pour visuels dynamiques et interactifs
    with tabs[2]:
        st.write("## Visuels Dynamiques et Interactifs")
        if st.session_state.processed_data:
            df = st.session_state.processed_data['df']
            # Sélection d'une variable numérique pour filtrer (si disponible)
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            if numeric_cols:
                variable = st.selectbox("Sélectionnez une variable numérique pour le filtrage :", options=numeric_cols)
                # Déterminer la plage de valeurs de la variable sélectionnée
                min_val = float(df[variable].min())
                max_val = float(df[variable].max())
                range_values = st.slider(f"Limitez la plage de la variable '{variable}' :", min_value=min_val, max_value=max_val, value=(min_val, max_val))
            else:
                variable = None
                range_values = None
            
            dynamic_query = st.text_area("Posez votre question pour le visuel dynamique (précisez si besoin le filtrage) :", value="")
            
            if dynamic_query and variable and range_values:
                if st.button("Générer le visuel dynamique"):
                    with st.spinner("Génération du visuel dynamique..."):
                        generate_dynamic_visualization(dynamic_query, variable, range_values)
        else:
            st.info("Chargez un dataset pour accéder aux visuels dynamiques.")
    
    with tabs[3]:
        st.write("## Historique des Requêtes")
        if st.session_state.history:
            for idx, entry in enumerate(st.session_state.history, start=1):
                with st.expander(f"Requête {idx}: {entry['query']}"):
                    st.markdown("**Type de visuel :** " + entry.get("viz_type", "Histogramme"))
                    st.markdown("**Thème appliqué :** " + entry.get("theme", "Standard"))
                    st.markdown("**Catégorie :** " + entry.get("type", "Générale"))
                    st.markdown("**Interprétation :**")
                    st.markdown(entry.get("interpretation", ""))
                    if st.button("Recharger cette visualisation", key=f"reload_{idx}"):
                        if entry.get("type", "Générale") == "Générale":
                            st.session_state.visualization_code = entry["visualization_code"]
                            st.session_state.viz_type = entry.get("viz_type", "Histogramme")
                            st.session_state.theme_choice = entry.get("theme", "Standard")
                            logo_url = get_logo_url(st.session_state.theme_choice)
                            st.image(logo_url, width=200)
                            display_dashboard()
                        else:
                            st.session_state.dynamic_visualization_code = entry["visualization_code"]
                            st.session_state.viz_type = entry.get("viz_type", "Visuel dynamique")
                            display_dynamic_dashboard()
        else:
            st.info("Aucune requête n'a été enregistrée.")

##############################
def process_data(uploaded_file):
    """Charge et traite le dataset."""
    df = DataLoader.load_data(uploaded_file)
    processor = DataProcessor(df)
    st.session_state.processed_data = {
        'df': processor.df,
        'summary': processor.get_summary()
    }

##############################
def generate_dataset_summary():
    """
    Utilise l'LLM pour générer un bref résumé du dataset à partir des noms de colonnes,
    en fournissant trois suggestions de visualisations pertinentes.
    """
    df = st.session_state.processed_data['df']
    client = ClaudeClient()
    
    prompt = f"""
    Tu es un expert en data analysis.
    Voici les noms des colonnes d'un dataset : {list(df.columns)}.
    Fournis un bref résumé du dataset en décrivant quelles informations pourraient être contenues et ce que ces variables indiquent.
    Ensuite, suggère trois types de visualisations pertinents à réaliser sur ce dataset, par exemple :
      1. Un histogramme pour observer la distribution d'une variable quantitative.
      2. Un scatter plot pour analyser la relation entre deux variables.
      3. Une heatmap pour visualiser les corrélations entre variables.
    Ne fournis que le résumé et les suggestions, sans code.
    """
    summary_text = client.generate_insights(prompt, data_summary={})
    st.session_state.dataset_summary = summary_text

##############################
def generate_visualization(query: str, viz_type: str):
    """
    Utilise l'LLM pour générer l'interprétation textuelle et le code complet de la visualisation générale.
    Le LLM doit choisir automatiquement la meilleure bibliothèque en fonction de la demande.
    Le code généré doit être complet, précis, sans balises ni commentaires, et prêt à être exécuté.
    """
    df = st.session_state.processed_data['df']
    client = ClaudeClient()
    full_query = query.strip()
    
    # Génération de l'interprétation textuelle
    data_summary = st.session_state.dataset_summary or ""
    interpretation_prompt = f"""
    Tu es un expert en data visualization en Python.
    Le dataset est chargé dans la variable 'df' et contient les colonnes : {list(df.columns)}.
    L'utilisateur a posé la question suivante pour obtenir une visualisation de type "{viz_type}" : "{full_query}".
    Fournis une courte interprétation textuelle décrivant ce que le graphique devrait montrer.
    Ne fournis que le texte, sans code.
    """
    interpretation_response = client.generate_insights(interpretation_prompt, data_summary={})
    
    # Génération du code de visualisation (le LLM choisira la bibliothèque la plus adaptée)
    code_prompt = f"""
    Tu es un expert en data visualization en Python.
    Le dataset est chargé dans la variable 'df' et contient les colonnes : {list(df.columns)}.
    L'utilisateur a posé la question suivante pour obtenir une visualisation de type "{viz_type}" : "{full_query}".
    Génère un snippet de code Python complet qui crée une visualisation pertinente à partir de 'df'.
    Choisis automatiquement la bibliothèque la plus adaptée.
    Assure-toi que le code utilise la variable 'df' et affecte le graphique à la variable 'fig'.
    Ne fournis que le code, sans aucun formatage, commentaires ou explications, et n'utilise pas de formatage de type %d.
    """
    code_snippet = client.generate_insights(code_prompt, data_summary={})
    
    try:
        st.session_state.insights = {
            "interpretation": json.loads(interpretation_response).get("analysis"),
            "code": code_snippet
        }
    except json.JSONDecodeError:
        st.session_state.insights = {
            "interpretation": interpretation_response,
            "code": code_snippet
        }
    
    st.session_state.visualization_code = code_snippet

##############################
def generate_dynamic_visualization(query: str, variable: str, range_values: tuple):
    """
    Génère un visuel dynamique/interactif en filtrant le dataset selon une variable numérique et une plage donnée.
    L'utilisateur fournit une question spécifique pour ce visuel dynamique.
    """
    df = st.session_state.processed_data['df']
    client = ClaudeClient()
    full_query = query.strip()
    
    # Génération de l'interprétation textuelle pour le visuel dynamique
    data_summary = st.session_state.dataset_summary or ""
    interpretation_prompt = f"""
    Tu es un expert en data visualization interactif en Python.
    Le dataset est chargé dans la variable 'df' et contient les colonnes : {list(df.columns)}.
    L'utilisateur souhaite créer un visuel dynamique de type "Interactif dynamique" pour filtrer les données de la variable "{variable}" entre {range_values[0]} et {range_values[1]}.
    La question posée est : "{full_query}".
    Fournis une courte interprétation textuelle décrivant ce que le graphique dynamique devrait montrer.
    Ne fournis que le texte, sans code.
    """
    interpretation_response = client.generate_insights(interpretation_prompt, data_summary={})
    
    # Génération du code du visuel dynamique
    code_prompt = f"""
    Tu es un expert en data visualization interactif en Python.
    Le dataset est chargé dans la variable 'df' et contient les colonnes : {list(df.columns)}.
    L'utilisateur souhaite créer un visuel dynamique de type "Interactif dynamique" pour filtrer les données de la variable "{variable}" entre {range_values[0]} et {range_values[1]}.
    La question posée est : "{full_query}".
    Génère un snippet de code Python complet qui crée une visualisation interactive pertinente à partir de 'df'
    en filtrant la variable "{variable}" dans la plage [{range_values[0]}, {range_values[1]}].
    Choisis automatiquement la bibliothèque la plus adaptée.
    Assure-toi que le code utilise la variable 'df' et affecte le graphique à la variable 'fig'.
    Ne fournis que le code, sans aucun formatage, commentaires ou explications.
    """
    code_snippet = client.generate_insights(code_prompt, data_summary={})
    
    try:
        st.session_state.insights = {
            "interpretation": json.loads(interpretation_response).get("analysis"),
            "code": code_snippet
        }
    except json.JSONDecodeError:
        st.session_state.insights = {
            "interpretation": interpretation_response,
            "code": code_snippet
        }
    
    st.session_state.dynamic_visualization_code = code_snippet
    # Enregistrer cette requête dans l'historique en tant que dynamique
    st.session_state.history.append({
        "query": query,
        "details": f"Filtrage sur '{variable}' entre {range_values[0]} et {range_values[1]}",
        "interpretation": st.session_state.insights.get("interpretation"),
        "visualization_code": st.session_state.dynamic_visualization_code,
        "viz_type": "Interactif dynamique",
        "theme": st.session_state.theme_choice,
        "type": "Dynamique"
    })
    display_dynamic_dashboard()

##############################
def display_dashboard():
    """
    Exécute le code généré pour afficher la visualisation générale.
    Seule la visualisation est affichée, pas le code.
    """
    st.write("## Visualisation générée")
    local_namespace = {'df': st.session_state.processed_data['df']}
    
    try:
        exec(st.session_state.visualization_code, {}, local_namespace)
        if 'fig' in local_namespace:
            st.plotly_chart(local_namespace['fig'], use_container_width=True)
        else:
            st.error("Le code généré n'a pas produit de variable 'fig'.")
    except Exception as e:
        st.error(f"Erreur lors de l'exécution du code généré : {e}")

##############################
def display_dynamic_dashboard():
    """
    Exécute le code généré pour afficher le visuel dynamique.
    Seul le visuel dynamique est affiché.
    """
    st.write("## Visuel Dynamique généré")
    local_namespace = {'df': st.session_state.processed_data['df']}
    
    try:
        exec(st.session_state.dynamic_visualization_code, {}, local_namespace)
        if 'fig' in local_namespace:
            st.plotly_chart(local_namespace['fig'], use_container_width=True)
        else:
            st.error("Le code généré n'a pas produit de variable 'fig' pour le visuel dynamique.")
    except Exception as e:
        st.error(f"Erreur lors de l'exécution du code généré pour le visuel dynamique : {e}")

##############################
if __name__ == "__main__":
    main()
