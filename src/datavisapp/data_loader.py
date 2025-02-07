import pandas as pd
from typing import Union
from .config import settings

class DataLoader:
    @staticmethod
    def load_data(file: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """Charge les données depuis différents formats"""
        if isinstance(file, pd.DataFrame):
            return file
        
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, nrows=settings.MAX_ROWS)
        elif file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file, nrows=settings.MAX_ROWS)
        elif file.name.endswith('.parquet'):
            df = pd.read_parquet(file)
        else:
            raise ValueError("Format de fichier non supporté")
            
        return df.sample(min(settings.SAMPLE_SIZE, len(df))).copy()