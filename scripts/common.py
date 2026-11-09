import os
from dotenv import load_dotenv

load_dotenv()

def get_config() -> tuple[str, str]:
    """Return (base_url, api_key)."""
    base_url = os.getenv("FORTYGUARD_BASE_URL", "https://api.fortyguard.com")
    api_key = os.getenv("FORTYGUARD_API_KEY")

    if not api_key:
        raise SystemExit("FORTYGUARD_API_KEY is not set. Check your .env file.")

    return base_url, api_key