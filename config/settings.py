import os

from dotenv import load_dotenv

load_dotenv()

GOREST_BASE_URL = os.getenv("GOREST_BASE_URL", "https://gorest.co.in/public/v2")
GOREST_TOKEN = os.getenv("GOREST_TOKEN")

if not GOREST_TOKEN:
    raise RuntimeError(
        "GOREST_TOKEN is not set. Copy .env.example to .env and add your GoRest "
        "personal access token (https://gorest.co.in/consumer/login), or export "
        "GOREST_TOKEN in your CI environment/secrets."
    )
