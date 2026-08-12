from datetime import datetime
import os
import csv
from report_webhook import request_types
import argparse
from dotenv import load_dotenv
from check_valid_parameters import  check_webhook_send, check_webhook_send, check_gym_nr
import sys
import requests
from club_requests import SendResponse
import re
from report_csv import report_csv
from clubs import club_addresses


load_dotenv("vars.env")

class config_static():
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
    
    
    def gym_number(self) -> list[int]:
        if not check_gym_nr():
            raise RuntimeError("Wrong gym numbers, use comma or space separated values with up to 105 values")
        
        if self.args.gym:
            gym_nrs = [int(match) for match in re.findall(r'\d+', ' '.join(self.args.gym))]
            return list(set(gym_nrs))
        else:
            gym_nr = os.getenv("GYM_NR")
            if gym_nr:
                gym_nrs = [int(match) for match in re.findall(r'\d+', ' '.join(self.args.gym))]
                return list(set(gym_nrs))
            else:
                return [1, 2, 3, 4]    





def main() -> int:
    send_request = request_types()
    config = config_static()
    gym_nr = config.gym_number()
    ppl_count = SendResponse().request_data(gym_nr)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    print("Logging results")
    
    if config.should_append_csv():
        print("Skipped csv append")
    else:
        report_csv(ppl_count, timestamp, gym_nr)
    
    if config.should_send_webhook():
        print("Skipped webhook")
    else:
        send_request.report_success(ppl_count)
    
    print("Done!")
    return 0

if __name__ == "__main__":
    main()
