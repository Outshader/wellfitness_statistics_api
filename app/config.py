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
        arg_skip = self.args.skip_csv
        env_skip = os.getenv("SAVE_TO_CSV", "true").lower() == "false"
        return arg_skip or env_skip
        
    def should_send_webhook(self) -> bool:
        if not check_webhook():
            print("WARNING: No webhook url given in envs.var. Forcing webhook skip.")
            return False
        arg_skip = self.args.skip_webhook
        env_skip = os.getenv("SEND_WEBHOOK", "true").lower() == "false" 
        return arg_skip or env_skip
    
    def parse_gym_ids(self):
        return [int(match) for match in re.findall(r'\d+', ' '.join(self.args.gym))]
    
    
    def get_gym_ids(self) -> list[int]:   
        if self.args.gym:
            gym_ids = self.parse_gym_ids()
            return list(set(gym_ids))
        else:
            gym_ids = os.getenv("GYM_IDS")
            if gym_ids and check_gym_ids(gym_ids):
                gym_ids = self.parse_gym_ids()
                return list(set(gym_ids))
            else:
                return [1, 2, 3, 4]