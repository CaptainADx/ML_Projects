import google.generativeai as genai
from dotenv import load_dotenv
import os;

load_dotenv()

# Paste your API key here
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List all available models
for model in genai.list_models():
    print(model.name)
