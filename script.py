from datetime import datetime
import os
import csv
from reports import ppl_count_not_found, report_success
import argparse
from dotenv import load_dotenv
from check_valid_parameters import  check_webhook_send, check_webhook_send, check_gym_nr
import sys
import requests
from clubs import club_addresses
from club_requests import request_data
import re

load_dotenv("vars.env")

class config_static():
    def __init__(self):
        load_dotenv("vars.env")
        parser = argparse.ArgumentParser()
        parser.add_argument('--skip-webhook', '-swh', action='store_true', help='Skip webhook usage')
        parser.add_argument('--skip-csv', '-scsv', action='store_true', help='Skip csv append usage')
        parser.add_argument('--gym', '-g', type=str, nargs="+", help='Which gym to pull data from')
        self.args = parser.parse_args()
    
    def should_append_csv(self):
        arg_skip = self.args.skip_csv
        env_skip = os.getenv("save_to_csv", "true").lower() == "false"
        return arg_skip or env_skip
        
    def should_send_webhook(self):
        arg_skip = self.args.skip_webhook
        env_skip = os.getenv("send_webhook", "true").lower() == "false"
        return arg_skip or env_skip
    
    def gym_number(self):
        if self.args.gym:
            return [int(match) for match in re.findall(r'\d+', ' '.join(self.args.gym))]
        else:
            gym_nr = os.getenv("gym_nr")
            if gym_nr:
                return [int(match) for match in re.findall(r'\d+', gym_nr)]
            else:
                return [1, 2, 3, 4]    


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


def main() -> int:
    config = config_static()
    gym_nr = config.gym_number()
    ppl_count = request_data()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    print("Logging results")
    
    if config.should_append_csv():
        print("Skipped csv append")
    else:
        csv_append(ppl_count, timestamp, gym_nr)
    
    if config.should_send_webhook():
        print("Skipped webhook")
    else:
        report_success(ppl_count)
    
    print("Done!")
    return 0

if __name__ == "__main__":
    main()
