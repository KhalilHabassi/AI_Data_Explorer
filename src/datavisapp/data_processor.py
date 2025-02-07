import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype

class DataProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.clean_data()
        
    def clean_data(self):
        """Nettoyage automatique des données"""
        # Suppression des colonnes vides
        self.df = self.df.dropna(axis=1, how='all')
        
        # Conversion des types de données
        for col in self.df.select_dtypes(include=['object']):
            try:
                self.df[col] = pd.to_datetime(self.df[col])
            except:
                pass
                
        # Gestion des valeurs manquantes
        for col in self.df.columns:
            if is_numeric_dtype(self.df[col]):
                self.df[col].fillna(self.df[col].median(), inplace=True)
            else:
                self.df[col].fillna(self.df[col].mode()[0], inplace=True)
    
    def get_summary(self) -> dict:
        """Retourne un résumé statistique des données"""
        return {
            'stats': self.df.describe().to_dict(),
            'missing_values': self.df.isna().sum().to_dict(),
            'dtypes': self.df.dtypes.astype(str).to_dict()
        }