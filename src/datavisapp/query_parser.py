QUESTION_TO_VIZ = {
    'distribution': [
        ("distribution de", "histogram"),
        ("fréquence des", "histogram"),
        ("répartition des", "composition")
    ],
    'correlation': [
        ("relation entre", "scatter"),
        ("corrélation", "heatmap"),
        ("liens entre", "scatter")
    ],
    'comparison': [
        ("comparer", "bar"),
        ("différence entre", "bar"),
        ("classement", "bar")
    ],
    'trend': [
        ("évolution", "line"),
        ("tendance", "line"),
        ("au fil du temps", "line")
    ],
    'geo': [
        ("par pays", "choropleth"),
        ("par région", "choropleth"),
        ("géographique", "choropleth")
    ]
}

def detect_visualization_type(question):
    """Détecte le type de visualisation depuis la question"""
    question = question.lower()
    for viz_type, patterns in QUESTION_TO_VIZ.items():
        for pattern in patterns:
            if pattern[0] in question:
                return viz_type, pattern[1]
    return 'distribution', 'histogram'  # Fallback