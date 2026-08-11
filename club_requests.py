import jwt
from datetime import datetime, timedelta
import requests
import dotenv
import os
from clubs import club_addresses
import json

dotenv.load_dotenv("vars.env")



def check_response(response: str) -> str:
    print("Errors" in response)
    if "Errors" in response:
        err_content = response["Errors"]
        msg_content = err_content[0]["Message"]
        
        if "login" in msg_content or "password" in msg_content:
            return "Login or password is incorrect"
    else:
        return ""

def get_password():
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
            
            
                

def refresh_token():
    email, password = os.getenv("EMAIL"), get_password()
    if not email or not password:
        raise RuntimeError("Well Fitness credentials missing")

    url = "https://wellfitness.perfectgym.pl/ClientPortal2/Auth/Login"
    headers = {"content-type": "application/json;charset=UTF-8", "accept-language": "en-US,en;q=0.5", "accept": "application/json, text/plain, */*", "cp-lang": "en", "x-hash": "#/Login", "x-requested-with": "XMLHttpRequest"}
    data_raw = {"RememberMe": "false", "Login": email, "Password": password}
    response = requests.post(
        url=url,
        json=data_raw,
        headers=headers,
    )
    
    json_response = response.json()
    valid_response = check_response(json_response)
    if valid_response:
        raise RuntimeError(valid_response)
    
    cookies = dict(response.cookies)
    authToken = cookies["CpAuthToken"]
    with open("token.txt", "w") as f:
        f.write(authToken)

    return 0
    
    
def jwt_exp(token):
    decode = jwt.decode(token, options={"verify_signature": False})
    exp_timestamp = decode["exp"]
    expiry_time = datetime.fromtimestamp(exp_timestamp)
    if ((expiry_time - datetime.now()) <= timedelta(0)):
        return True
    else:
        return False
    

def get_token() -> str:
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as f:
            return f.readline()
    else:
        return ""
        
        
        
def parse_response(data: dict, gym_nr: list) -> list:
    addresses = []
    for i in gym_nr:
        addresses.append(club_addresses[i])
        
    gym_count = {}
    for club_info in data["UsersInClubList"]:
        if club_info["ClubAddress"] in addresses:
            gym_count[club_info["ClubAddress"]] = club_info["UsersCountCurrentlyInClub"]
        
    return gym_count
        
        
def request_data(gym_nr: list) -> dict:
    print("Reading token from token.txt")
    token = get_token()
    
    print("Checking token expiration date")
    if not token or jwt_exp(token):
        print("Token does not exist, renewing")
        refresh_token()
        token = get_token()
        print("Token renewed")
        

    url = "https://wellfitness.perfectgym.com/ClientPortal2/Clubs/Clubs/GetMembersInClubs"
    cookies = {
        "CpAuthToken": token,
    }
    response = requests.post(url, cookies=cookies)
    parsed_response = parse_response(response.json(), gym_nr)
    return parsed_response


if __name__ == "__main__":
    print(request_data())