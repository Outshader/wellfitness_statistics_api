import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

import dotenv

dotenv.load_dotenv(ROOT_DIR / "vars.env")


def check_gym_ids(gym_ids):
    try: 
        gym_ids = gym_ids.split(",")
        how_many = 0
        for gym_id in gym_ids:
            how_many += 1 
            int(gym_id)
        if how_many > 105:
            return False

    except ValueError:
        return False
    return True


def check_webhook():
    webhook = os.getenv("WEBHOOK_URL", "")
    if not ("https://discordapp.com/api/webhooks/" in webhook):
        return False
    return True



