import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Locate the project directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env from the project directory
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Retrieve API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        f"Gemini API key not found in {ENV_PATH}"
    )

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Model selection
MODEL_NAME = "gemini-3.5-flash-lite"