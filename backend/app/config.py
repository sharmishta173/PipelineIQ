from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

AZURE_ORG = os.getenv("AZURE_ORG")
AZURE_PROJECT = os.getenv("AZURE_PROJECT")
AZURE_PAT = os.getenv("AZURE_PAT")

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")