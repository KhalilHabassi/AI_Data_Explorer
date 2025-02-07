import json
from anthropic import Anthropic
from .config import settings

class ClaudeClient:
    def __init__(self):
        self.client = Anthropic(api_key=settings.CLAUDE_API_KEY)
    
    def generate_insights(self, prompt: str, data_summary: dict):
        """
        Envoie le prompt à Claude et retourne la réponse textuelle.
        Ce mécanisme est utilisé pour générer du texte, que ce soit une interprétation ou un snippet de code.
        """
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=settings.MAX_TOKENS,
            system=prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        if response and response.content:
            return response.content[0].text
        return "Aucune réponse générée."
