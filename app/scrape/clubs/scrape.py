from datetime import datetime
from pathlib import Path
from .parse import ParseResponse

ROOT_DIR = Path(__file__).resolve().parents[3]

import jwt
import requests

from app.scrape.clubs.parse import ValidateConfig


class ValidateToken():
    def __init__(self):
        self.token = self.get_token()

        
    def get_token(self) -> str:
        print("Reading token from token.txt")
        token = self.read_token()
        
        print("Checking token expiration date")
        if not token or self.jwt_exp(token):
            print("Token does not exist, renewing")
            self.refresh_token(ValidateConfig().email, ValidateConfig().password)
            token = self.read_token()
            print("Token renewed")
        return token
    
    def read_token(self) -> str:
        token_path = ROOT_DIR / "data" / "token.txt"
        if token_path.exists():
            with open(token_path, "r") as f:
                return f.readline()
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
        valid_response = ParseResponse().check_response(response)
        if valid_response:
            raise RuntimeError(valid_response)
        
        cookies = dict(response.cookies)
        authToken = cookies["CpAuthToken"]
        with open(ROOT_DIR / "data" / "token.txt", "w") as f:
            f.write(authToken)
    
    def jwt_exp(self, token: str) -> bool:
        decode = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = decode["exp"]
        expiry_time = datetime.fromtimestamp(exp_timestamp)
        is_expired = expiry_time <= datetime.now()
        if is_expired:
            return True
        else:
            return False



class ResponseHandling():
    def __init__(self):
        self.token = ValidateToken().token

            
    def request_data(self, gym_ids: list[int]) -> dict:
        url = "https://wellfitness.perfectgym.com/ClientPortal2/Clubs/Clubs/GetMembersInClubs"
        cookies = {
            "CpAuthToken": self.token,
        }
        response = requests.post(url, cookies=cookies)
        parsed_response = ParseResponse().parse_response(data=response.json(), gym_ids=gym_ids)
        return parsed_response

