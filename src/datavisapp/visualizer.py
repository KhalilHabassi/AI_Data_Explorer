import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Visualizer:
    def __init__(self, df):
        self.df = df
        self.color_scale = px.colors.sequential.Viridis

    def create_visualization(self, viz_type, params):
        """Route vers le template approprié"""
        templates = {
            'distribution': self._distribution_chart,
            'correlation': self._correlation_chart,
            'composition': self._composition_chart,
            'comparison': self._comparison_chart,
            'trend': self._trend_chart,
            'geo': self._geo_chart
        }
        if viz_type not in templates:
            raise ValueError(f"Le type de visualisation '{viz_type}' n'est pas supporté.")
        return templates[viz_type](**params)

    def _distribution_chart(self, column, bins=10):
        """Distribution d'une variable"""
        return px.histogram(
            self.df, 
            x=column, 
            nbins=bins,
            color_discrete_sequence=[self.color_scale[2]],
            marginal='box',
            title=f"Distribution de {column}"
        )

    def _correlation_chart(self, x, y, color=None):
        """Corrélation entre deux variables"""
        return px.scatter(
            self.df, 
            x=x, y=y, 
            color=color,
            trendline='lowess',
            color_continuous_scale=self.color_scale,
            title=f"Corrélation entre {x} et {y}"
        )

    def _composition_chart(self, column, threshold=0.01):
        """Composition (camembert/treemap)"""
        counts = self.df[column].value_counts(normalize=True)
        filtered = counts[counts > threshold]
        if len(filtered) < 5:
            return px.pie(filtered, names=filtered.index, values=filtered.values, title=f"Composition de {column}")
        else:
            return px.treemap(filtered, path=[filtered.index], values=filtered.values, title=f"Composition de {column}")

    def _comparison_chart(self, x, y, type='bar'):
        """Comparaison de catégories"""
        if type == 'bar':
            return px.bar(self.df, x=x, y=y, color=x, title=f"Comparaison de {x} et {y}")
        elif type == 'radar':
            return px.line_polar(self.df, r=y, theta=x, line_close=True, title=f"Comparaison (Radar) de {x} et {y}")

    def _trend_chart(self, date_column, value_column, freq='M'):
        """Tendance temporelle"""
        df_resampled = self.df.set_index(date_column).resample(freq).mean()
        return px.area(df_resampled, y=value_column, line_shape='spline', title=f"Tendance de {value_column} au fil du temps")

    def _geo_chart(self, geo_column, value_column):
        """Carte géographique"""
        return px.choropleth(
            self.df,
            locations=geo_column,
            locationmode='country names',
            color=value_column,
            color_continuous_scale=self.color_scale,
            title=f"Carte géographique de {value_column}"
        )

def get_visualization_template(chart_type: str):
    templates = {
        "histogramme": "generate_histogram",
        "courbe": "generate_line_chart",
        "toile d'araignée": "generate_spider_chart",
        # Vous pouvez ajouter d'autres mappings si nécessaire
    }
    return templates.get(chart_type.lower())

# Pour que les méthodes attendues par get_visualization_template existent,
# on peut ajouter ces alias dans la classe Visualizer.
def generate_histogram(self, x: str, color: str = None):
    return px.histogram(
        self.df, 
        x=x, 
        color=color, 
        title=f"Histogramme de {x} par {color}" if color else f"Histogramme de {x}"
    )

def generate_line_chart(self, x: str, y: str):
    return px.line(
        self.df, 
        x=x, y=y, 
        title=f"Courbe de {y} en fonction de {x}"
    )

def generate_spider_chart(self, columns: list):
    values = [self.df[col].mean() for col in columns]
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=columns,
        fill='toself'
    ))
    fig.update_layout(title="Toile d'araignée", polar=dict(radialaxis=dict(visible=True)))
    return fig

# Attacher ces fonctions à la classe Visualizer
Visualizer.generate_histogram = generate_histogram
Visualizer.generate_line_chart = generate_line_chart
Visualizer.generate_spider_chart = generate_spider_chart
