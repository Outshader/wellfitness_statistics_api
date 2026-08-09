import jwt
from datetime import datetime, timedelta
import requests
import dotenv
import os

dotenv.load_dotenv()



def refresh_token():
    email, password = os.getenv("email"), rf'{os.getenv("password")}'
    url = "https://wellfitness.perfectgym.pl/ClientPortal2/Auth/Login"
    headers = {"content-type": "application/json;charset=UTF-8"}
    data_raw = {"RememberMe": "false", "Login": email, "Password": password}
    response = requests.post(
        url=url, 
        json=data_raw,
        headers=headers
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
    return ((expiry_time - datetime.now()) <= timedelta(0))
    

def get_token():
    with open("token.txt", "r") as f:
        return f.readline()

def request_data():
    print("Reading token from token.txt")
    token = get_token()
    
    print("Checking token expiration date")
    expired = jwt_exp(token)
    if expired:
        print("Token has expired, renewing")
        refresh_token()
        token = get_token()
        print("Token renewed")
        
    url = "https://wellfitness.perfectgym.com/ClientPortal2/Clubs/Clubs/GetMembersInClubs"
    cookies = {
        "CpAuthToken": token,
    }
    response = requests.post(url, cookies=cookies)
    return response.json()


if __name__ == "__main__":
    print(request_data())