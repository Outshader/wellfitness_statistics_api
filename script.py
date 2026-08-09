from datetime import datetime
import os
import csv
from webhook_report import ppl_count_not_found, report_success
import argparse
from dotenv import load_dotenv
from check_valid_parameters import  check_webhook_send, check_gym_nr
import sys
import requests
from clubs import club_addresses
from club_requests import request_data

load_dotenv("vars.env")








    


APP = "com.perfectgym.perfectgymgo2.wellfitness"
APP_ACTIVITY = "/com.elpassion.perfectgym.splash.SplashActivity"


def arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-webhook', '-swh', action='store_false', help='Skip webhook usage, both for ALL reports. Off by default')
    parser.add_argument('--skip-csv', '-scsv', action='store_false', help='Skip csv append usage. Off by default')
    parser.add_argument('--gym', '-g', type=str, default=[1], nargs="+", help='Which gym to pull data from')
    return parser.parse_args()
        


    
def parse_response(data: dict, gym_nr: list) -> list:
    addresses = []
    try:
        for i in gym_nr:
            addresses.append(club_addresses[i])
    except TypeError:
        addresses.append(club_addresses[gym_nr])
        
    gym_count = {}
    for club_info in data["UsersInClubList"]:
        if club_info["ClubAddress"] in addresses:
            gym_count[club_info["ClubAddress"]] = club_info["UsersCountCurrentlyInClub"]
    return gym_count
    


def csv_append(ppl_count: int, timestamp: str, gyms: list) -> int:
    with open("logs.csv", "a", newline="", encoding="utf-8") as file:
        fieldnames = ["Club name", "date_time", "ppl_count"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for i in gyms:
            club_name = club_addresses[i]
            writer.writerow({
                "Club name": club_name, 
                "date_time": timestamp, 
                "ppl_count": ppl_count[club_name]
            })
        
    return 0


def get_gym_nr(args) -> list:
    if args.gym: 
        return list(map(int,args.gym))
    elif check_gym_nr():
        gym_nr = os.getenv("gym_nr")
        gym_nr = gym_nr.split(",")
        gym_nr = list(map(int, gym_nr))
        return gym_nr
    else:
        return [1,2,3,4]
        
        


def main() -> int:
    args = arguments_parser()
    print(args)
    gym_nr = get_gym_nr(args)
    ppl_count_data = request_data()
    ppl_count = parse_response(ppl_count_data, gym_nr)
    
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    print("Logging results")
    if args.skip_csv:
        csv_append(ppl_count, timestamp, gym_nr)
    print(f"Skipped csv would've printed: \n")
    print(ppl_count, timestamp, gym_nr)
    print("Reporting success!")
    if args.skip_webhook:
        report_success(ppl_count)
    print("Done!")
    return 0





if __name__ == "__main__":
    main()
