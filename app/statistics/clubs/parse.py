import os
import csv
from pathlib import Path
import dotenv
import requests

ROOT_DIR = Path(__file__).resolve().parents[3]

from app.config import config
from app.reports.webhook import RequestTypes

# data directory is at the repository root: <repo>/data
DATA_ROOT = ROOT_DIR / "data"

dotenv.load_dotenv(ROOT_DIR / "vars.env")

class ParseResponse():
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

        return gym_data        
    
    def check_response(self, response: requests.models.Response) -> str:
        json_content = response.json()
        cookies = response.cookies
        token = cookies["CpAuthToken"] or ""
        if not token:
            err_content = json_content["Errors"]
            if "Errors" in json_content:
                msg_content = err_content[0]["Message"]
                if "login" in msg_content or "password" in msg_content:
                    return "Login or password is incorrect"
                else:
                    return msg_content
                
            else:
                return f"Something went wrong \n error content:\n {err_content}, json_content: \n{json_content}, Cookies:\n {cookies}"
        else:
            return ""


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
    


    
    
