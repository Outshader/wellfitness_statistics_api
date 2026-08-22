import os
import argparse
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

import dotenv

from app.validate_parameters import check_gym_ids, check_webhook


class config():
    def __init__(self):
        dotenv.load_dotenv(ROOT_DIR / "vars.env")
        parser = argparse.ArgumentParser()
        parser.add_argument('--skip-webhook', '-swh', action='store_true', help='Skip webhook usage')
        parser.add_argument('--skip-csv', '-scsv', action='store_true', help='Skip csv append usage')
        parser.add_argument('--gym', '-g', type=str, nargs="+", help='Which gym to pull data from')
        self.args = parser.parse_args()
    
    def should_append_csv(self) -> bool:
        if getattr(self.args, 'skip_csv', False):
            return True
        
        save_to_csv = os.getenv("SAVE_TO_CSV", "true").strip().lower()
        return True if save_to_csv == "false" else False
        
    def should_send_webhook(self) -> bool:
        if not check_webhook():
            print("WARNING: No webhook url given in envs.var. Forcing webhook skip.")
            return True
        
        if getattr(self.args, 'skip_webhook', False):
            return True
        
        send_webhook = os.getenv("SEND_WEBHOOK", "true").strip().lower()
        return True if send_webhook == "false" else False
    
    def parse_gym_ids(self, src: str) -> list[int]:
        if not src:
            return []
        return [int(match) for match in re.findall(r'\d+', src)]
    
    def get_gym_ids(self) -> list[int]:
        args_gym = getattr(self.args, 'gym', None)
        if args_gym:
            args_gym = ', '.join(args_gym)
            ids = self.parse_gym_ids(args_gym)
            # deletes the duplicates from ids and makes it into a list
            return list(dict.fromkeys(ids))

        gym_ids_env = os.getenv("GYM_IDS", "")
        if gym_ids_env and check_gym_ids(gym_ids_env):
            ids = self.parse_gym_ids(gym_ids_env)
            return list(dict.fromkeys(ids))

        return [1, 2, 3, 4]