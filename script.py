from datetime import datetime
import os
import csv
from report_webhook import request_types
import argparse
from dotenv import load_dotenv
from check_valid_parameters import  check_webhook_send, check_webhook_send, check_gym_ids
import sys
import requests
from club_requests import ResponseHandling
import re
from report_csv import report_csv_append
from clubs import club_addresses


load_dotenv("vars.env")

class config():
    def __init__(self):
        load_dotenv("vars.env")
        parser = argparse.ArgumentParser()
        parser.add_argument('--skip-webhook', '-swh', action='store_true', help='Skip webhook usage')
        parser.add_argument('--skip-csv', '-scsv', action='store_true', help='Skip csv append usage')
        parser.add_argument('--gym', '-g', type=str, nargs="+", help='Which gym to pull data from')
        self.args = parser.parse_args()
    
    def should_append_csv(self) -> bool:
        arg_skip = self.args.skip_csv
        env_skip = os.getenv("SAVE_TO_CSV", "true").lower() == "false"
        return arg_skip or env_skip
        
    def should_send_webhook(self) -> bool:
        arg_skip = self.args.skip_webhook
        env_skip = os.getenv("SEND_WEBHOOK", "true").lower() == "false" 
        return arg_skip or env_skip
    
    
    def get_gym_ids(self) -> list[int]:   
        if self.args.gym:
            gym_ids = [int(match) for match in re.findall(r'\d+', ' '.join(self.args.gym))]
            return list(set(gym_ids))
        else:
            gym_ids = os.getenv("GYM_IDS")
            if gym_ids and check_gym_ids(gym_ids):
                gym_ids = [int(match) for match in re.findall(r'\d+', ' '.join(self.args.gym))]
                return list(set(gym_ids))
            else:
                return [1, 2, 3, 4]


class MainOrchestrator():
    def __init__(self):
        self.send_request = request_types()
        self.send_response = ResponseHandling()
        self.config = config()
        self.gym_ids = config.get_gym_ids()
    
    def main() -> int:
        gym_data = send_response.request_data(gym_id)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        
        print("Logging results")
        
        if config.should_append_csv():
            print("Skipped csv append")
        else:
            report_csv(gym_data, timestamp, gym_id)
        
        if config.should_send_webhook():
            print("Skipped webhook")
        else:
            send_request.report_success(gym_data)
        
        print("Done!")
        return 0

if __name__ == "__main__":
    MainOrchestrator().main()
