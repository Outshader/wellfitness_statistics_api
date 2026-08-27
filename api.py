import csv
import os
import requests
from config import Config

class Clubs():
    
    def parse_response(self, data: dict, gym_ids: list[int]) -> dict[str, str]:
        with open("data/clubs.csv", encoding="utf-8", mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            names = []
            
            for row in rows:
                if row and int(row["ID"]) in gym_ids:
                    names.append(row["club_name"].strip())
                    
            
        gym_data = {}
        for club_info in data["UsersInClubList"]:
            if club_info["ClubName"] in names:
                gym_data[club_info["ClubName"]] = club_info["UsersCountCurrentlyInClub"]

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
        invalid_response = self.check_response(response)
        if invalid_response:
            raise RuntimeError(invalid_response)
        
        cookies = dict(response.cookies)
        authToken = cookies["CpAuthToken"]
        os.environ["AUTH_TOKEN"] = authToken

        
    def clubs_main(self, gym_ids: list[int]) -> dict:
        url = "https://wellfitness.perfectgym.com/ClientPortal2/Clubs/Clubs/GetMembersInClubs"
        cookies = {
            "CpAuthToken": Config().token
        }
        response = requests.post(url, cookies=cookies)
        try:
            parsed_response = self.parse_response(data=response.json(), gym_ids=gym_ids)
        except requests.exceptions.JSONDecodeError:
            raise requests.exceptions.JSONDecodeError
        
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