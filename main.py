import os
import argparse
import re
from pathlib import Path
import dotenv
from datetime import datetime
import jwt
from api import Clubs
from reports import Csv, Webhook




class Config():
    def __init__(self):
        dotenv.load_dotenv("data" / "vars.env")
        parser = argparse.ArgumentParser()
        parser.add_argument('--skip-webhook', '-swh', action='store_true', help='Skip webhook usage')
        parser.add_argument('--skip-csv', '-scsv', action='store_true', help='Skip csv append usage')
        parser.add_argument('--gym', '-g', type=str, nargs="+", help='Which gym to pull data from')
        self.args = parser.parse_args()
        self.gym_ids = self._get_gym_ids()
        self.skip_webhook = self._skip_webhook()
        self.skip_csv = self._skip_csv
        self.email, self.password = self._get_credentials()
        self.token = self._get_token
        
    def _check_gym_ids(self, gym_ids):
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
    
    def _parse_gym_ids(self, src: str) -> list[int]:
        if not src:
            return []
        return [int(match) for match in re.findall(r'\d+', src)]
    
    def _get_gym_ids(self) -> list[int]:
        args_gym = getattr(self.args, 'gym', None)
        if args_gym:
            args_gym = ', '.join(args_gym)
            ids = self._parse_gym_ids(args_gym)
            # deletes the duplicates from ids and makes it into a list
            return list(dict.fromkeys(ids))

        gym_ids_env = os.getenv("GYM_IDS", "")
        if gym_ids_env and self._check_gym_ids(gym_ids_env):
            ids = self._parse_gym_ids(gym_ids_env)
            return list(dict.fromkeys(ids))

        return [1, 2, 3, 4]


    def _check_webhook(self):
        webhook = os.getenv("WEBHOOK_URL", "")
        if not ("https://discordapp.com/api/webhooks/" in webhook):
            return False
        return True
    
    def _skip_webhook(self) -> bool:
        if not self._check_webhook():
            print("WARNING: No webhook url given in envs.var. Forcing webhook skip.")
            return True
        
        if getattr(self.args, 'skip_webhook', False):
            return True
        
        send_webhook = os.getenv("SEND_WEBHOOK", "true").strip().lower()
        return True if send_webhook == "false" else False
    
    
    def _skip_csv(self) -> bool:
        if getattr(self.args, 'skip_csv', False):
            return True
        
        save_to_csv = os.getenv("SAVE_TO_CSV", "true").strip().lower()
        return True if save_to_csv == "false" else False
        

    
                
    def _get_credentials(self) -> tuple[str, str]:
        email = os.getenv("EMAIL", "")
        password = ""
        with open("vars.env", "r") as f:
            data = f.readlines()
            for i in data:
                if "PASSWORD" in i:
                    password = i.strip().split("=", 1)[-1]
                    first_char, last_char = password[0], password[-1]
                    if first_char == last_char:
                        password = password.strip(f"{first_char}")
                        
        if not email or not password:
            raise RuntimeError("Well Fitness credentials missing")
        return email, password
    
    
    def _get_token(self) -> str:
        print("Reading token from token.txt")
        token = self._read_token()
        
        print("Checking token expiration date")
        if not token or self._jwt_exp(token):
            print("Token does not exist, renewing")
            Clubs().refresh_token(self.email, self.password)
            token = self._read_token()
            print("Token renewed")
        return token
            
    
    def _read_token(self) -> str:
            token_path = "data" / "token.txt"
            if token_path.exists():
                with open(token_path, "r") as f:
                    return f.readline()
            else:
                return ""

    def _jwt_exp(self, token: str) -> bool:
        decode = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = decode["exp"]
        expiry_time = datetime.fromtimestamp(exp_timestamp)
        is_expired = expiry_time <= datetime.now()
        if is_expired:
            return True
        else:
            return False
    
    
class Main():
    def __init__(self):
        self.gym_ids = Config().gym_ids
    
    def main(self) -> None:
        gym_data = Clubs().clubs_main(self.gym_ids)
        print(gym_data)
        timestamp = datetime.now().isoformat()
        
        print("Logging results")
        
        if Config().skip_csv:
            print("Skipped csv append")
        else:
            Csv().report_csv_append(gym_data, timestamp)
        
        if Config().skip_webhook:
            print("Skipped webhook")
        else:
            Webhook().report_success(gym_data)
        print("Subtracting class data")
        # class_data_main()
        
        print("Done!")