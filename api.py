from pathlib import Path
import requests
from datetime import datetime
import csv
import jwt
from main import Config

ROOT_DIR = Path(__file__).resolve().parents[3]

DATA_ROOT = ROOT_DIR / "data"

class Clubs():
    def __init__(self):
        self.token = Config().token
    
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
        

    def refresh_token(self, email: str, password: str) -> None:
        url = "https://wellfitness.perfectgym.pl/ClientPortal2/Auth/Login"
        headers = {"content-type": "application/json;charset=UTF-8"}
        data_raw = {"RememberMe": "false", "Login": email, "Password": password}
        response = requests.post(
            url=url,
            json=data_raw,
            headers=headers,
        )
        valid_response = self.check_response(response)
        if valid_response:
            raise RuntimeError(valid_response)
        
        cookies = dict(response.cookies)
        authToken = cookies["CpAuthToken"]
        with open(ROOT_DIR / "data" / "token.txt", "w") as f:
            f.write(authToken)

        
    def clubs_main(self, gym_ids: list[int]) -> dict:
        url = "https://wellfitness.perfectgym.com/ClientPortal2/Clubs/Clubs/GetMembersInClubs"
        cookies = {
            "CpAuthToken": self.token,
        }
        response = requests.post(url, cookies=cookies)
        parsed_response = self.parse_response(data=response.json(), gym_ids=gym_ids)
        return parsed_response




class Classes():
    def scrape_classes(self):
        response = requests.post(
            url="https://wellfitness.perfectgym.com/ClientPortal2/Classes/ClassCalendar/WeeklyClasses",
            json={"clubId": 17, "categoryId": None, "timeTableId": None, "trainerId": None, "daysInWeek": 2, "QueryStartDate": "2026-08-17"},
            headers={
                "accept": "application/json",
                "x-requested-with": "XMLHttpRequest",
                "cp-lang": "pl",
                "cp-mode": "desktop"
            }
        )
        return response.json()