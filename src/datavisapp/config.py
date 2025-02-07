from pathlib import Path
import configparser
import os
from dotenv import load_dotenv

# Chemin ABSOLU du projet (à adapter si besoin)
BASE_DIR = Path(__file__).parent.parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(env_path)

# Charger la configuration depuis un fichier settings.toml
config = configparser.ConfigParser()
config_path = BASE_DIR / 'settings.toml'
config.read(config_path)

print(f"Chemin config : {config_path}")
print(f"Sections config : {config.sections()}")

class Settings:
    # Data Processing
    MAX_ROWS = int(config['DATA'].get('MAX_ROWS', '10000'))
    SAMPLE_SIZE = int(config['DATA'].get('SAMPLE_SIZE', '1000'))
    
    # Visualization
    DEFAULT_THEME = config['VIZ'].get('DEFAULT_THEME', 'plotly_white')
    COLOR_SCHEME = config['VIZ'].get('COLOR_SCHEME', 'Viridis')
    
    # LLM
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    MAX_TOKENS = int(config['LLM'].get('MAX_TOKENS', '1000'))
    TEMPERATURE = float(config['LLM'].get('TEMPERATURE', '0.7'))

settings = Settings()
