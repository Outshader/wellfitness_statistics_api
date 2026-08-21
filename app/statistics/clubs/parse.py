import os
import csv
from pathlib import Path
import dotenv

ROOT_DIR = Path(__file__).resolve().parents[3]

from app.config import config
from app.reports.webhook import RequestTypes

DATA_ROOT = ROOT_DIR / "app" / "data"

dotenv.load_dotenv(ROOT_DIR / "vars.env")

class ValidateResponse():
    def validate_response(self, gym_ids: list[int], gym_data: dict[str, int]) -> None:
        if len(gym_data) != len(gym_ids):
            if config().should_send_webhook():
                RequestTypes().report_other_error_occured("Parsing of the response data failed! The report webhook was sent")
                raise RuntimeError("Parsing of the response data failed! The report webhook was sent")
            else: 
                raise RuntimeError("Parsing of the response data failed! The report webhook was not sent")
    
    
    def parse_response(self, data: dict, gym_ids: list[int]) -> dict[str, str]:
        with open(DATA_ROOT / "clubs.csv", encoding="utf-8", mode="r") as file:
            reader = csv.DictReader(file, fieldnames=["ID", "club_name", "club_address"])            
            rows = list(reader)
            addresses = []
            
            for row in rows:
                for gym_id in gym_ids:
                    if row["ID"] == gym_id:
                        addresses.append(row["club_address"])
                        continue
            
        gym_data = {}
        for club_info in data["UsersInClubList"]:
            if club_info["ClubAddress"] in addresses:
                gym_data[club_info["ClubAddress"]] = club_info["UsersCountCurrentlyInClub"]

        self.validate_response(gym_ids, gym_data)
        return gym_data        


class ValidateConfig():
    def __init__(self):
        self.email, self.password = self.get_credentials()

    def get_password(self):
        with open(ROOT_DIR / "vars.env", "r") as f:
            data = f.readlines()
            for i in data:
                if "PASSWORD" in i:
                    password = i.strip().split("=", 1)[1]
                    first_char, last_char = password[0], password[-1]
                    if first_char == last_char:
                        password = password.strip(f"{first_char}")
                    return password
                
    def get_credentials(self) -> tuple[str, str]:
        email, password = os.getenv("EMAIL", ""), self.get_password()
        if not email or not password:
            raise RuntimeError("Well Fitness credentials missing")
        return email, password
    


    
    
