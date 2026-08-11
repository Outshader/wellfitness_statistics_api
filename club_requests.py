import jwt
from datetime import datetime, timedelta
import requests
import dotenv
import os
from clubs import club_addresses

dotenv.load_dotenv()



def refresh_token():
    email = os.getenv("email")
    password = os.getenv("password")
    if not email or not password:
        raise RuntimeError("Well Fitness credentials missing")

    url = "https://wellfitness.perfectgym.pl/ClientPortal2/Auth/Login"
    headers = {"content-type": "application/json;charset=UTF-8"}
    data_raw = {"RememberMe": "false", "Login": email, "Password": password}
    response = requests.post(
        url=url,
        json=data_raw,
        headers=headers,
        timeout=30,
    )

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
    

def get_token():
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as f:
            return f.readline()
    else:
        return False
        
        
        
def parse_response(data: dict, gym_nr: list) -> list:
    addresses = []
    for i in gym_nr:
        addresses.append(club_addresses[i])
        
    gym_count = {}
    for club_info in data["UsersInClubList"]:
        if club_info["ClubAddress"] in addresses:
            gym_count[club_info["ClubAddress"]] = club_info["UsersCountCurrentlyInClub"]
    return gym_count
        
        
        
def request_data():
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
    parsed_response = parse_response(response.json())
    return parsed_response


if __name__ == "__main__":
    print(request_data())