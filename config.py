import os
from dotenv import load_dotenv

load_dotenv()

class EnvConfig():
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        
env_config = EnvConfig()
