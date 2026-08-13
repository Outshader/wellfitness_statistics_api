import jwt
from datetime import datetime, timedelta
import requests
import dotenv
import os
from clubs import club_addresses
import json
from report_webhook import request_types

dotenv.load_dotenv("vars.env")

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
        if os.path.exists("token.txt"):
            with open("token.txt", "r") as f:
                return f.readline()
        else:
            return ""
    
    def check_response(self, response: str) -> str:
        json_content, cookies = response.json(), response.cookies
        if "CpAuthToken" not in cookies or len(cookies["CpAuthToken"]) == 0:
            if "Errors" in json_content:
                err_content = json_content["Errors"]
                msg_content = err_content[0]["Message"]
                if "login" in msg_content or "password" in msg_content:
                    return "Login or password is incorrect"
                else:
                    return msg_content
                
            else:
                return f"Something went wrong \n error content:\n {err_content}, json_content: \n{json_content}, Cookies:\n {cookies}"
        else:
            return ""
    
    
    def refresh_token(self, email: str, password: str) -> int:
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
        with open("token.txt", "w") as f:
            f.write(authToken)
        return 0
    
    def jwt_exp(token: str) -> bool:
        decode = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = decode["exp"]
        expiry_time = datetime.fromtimestamp(exp_timestamp)
        if ((expiry_time - datetime.now()) <= timedelta(0)):
            return True
        else:
            return False



class ValidateConfig():
    def __init__(self):
        self.email, self.password = self.get_credentials()

    def get_password(self):
        with open("vars.env", "r") as f:
            data = f.readlines()
            for i in data:
                if "PASSWORD" in i:
                    password = i.strip().split("=", 1)
                    break

            password = password[1]
            first, last = password[0], password[-1]
            if first == last:
                password = password.strip(f"{first}")
            return password

    def get_credentials(self) -> tuple[str, str]:
        email, password = os.getenv("EMAIL", ""), self.get_password()
        if not email or not password:
            raise RuntimeError("Well Fitness credentials missing")
        return email, password
    


    
    
class ResponseHandling():
    def __init__(self):
        token_class = ValidateToken()
        self.token = token_class.token
            
    def validate_response(gym_data: dict, addresses: list) -> dict:
        if len(gym_data) != len(gym_id):
            if not config.should_send_webhook():
                sys.exit("Parsing of the response data failed! The report webhook was not sent")
            else: 
                send_request.report_ppl_count_not_found("Parsing of the response data failed! The report webhook was sent")
                sys.exit("Parsing of the response data failed! The report webhook was sent")
        return 0
    
    
    def parse_response(self, data: dict, gym_id: list) -> dict[str, str]:
        addresses = []
        for i in gym_id:
            addresses.append(club_addresses[i])
            
        gym_data = {}
        for club_info in data["UsersInClubList"]:
            if club_info["ClubAddress"] in addresses:
                gym_data[club_info["ClubAddress"]] = club_info["UsersCountCurrentlyInClub"]

        self.validate_response(gym_data, addresses)
        return gym_data        

            
    def request_data(self, gym_id: list) -> dict:
        url = "https://wellfitness.perfectgym.com/ClientPortal2/Clubs/Clubs/GetMembersInClubs"
        cookies = {
            "CpAuthToken": self.token,
        }
        response = requests.post(url, cookies=cookies)
        parsed_response = self.parse_response(response.json(), gym_id)
        return parsed_response


if __name__ == "__main__":
    obj = SendResponse()
    print(obj.parse_response())