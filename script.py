from datetime import datetime
import os
from report_webhook import RequestTypes
import argparse
from dotenv import load_dotenv
from validate_parameters import check_gym_ids, check_webhook
from club_requests import ResponseHandling
import re
from report_csv import report_csv_append
from config import config

load_dotenv("vars.env")



class Main():
    def __init__(self):
        self.send_webhook_report = RequestTypes()
        self.get_gym_data = ResponseHandling()
        self.gym_ids = config().get_gym_ids()
    
    def main(self) -> None:
        gym_data = self.get_gym_data.request_data(self.gym_ids)
        timestamp = datetime.now().strftime("%Y-%m-%A_%H-%M")
        
        print("Logging results")
        
        if config().should_append_csv():
            print("Skipped csv append")
        else:
            report_csv_append(gym_data, timestamp)
        
        if config().should_send_webhook():
            print("Skipped webhook")
        else:
            self.send_webhook_report.report_success(gym_data)
        
        print("Done!")

if __name__ == "__main__":
    Main().main()
