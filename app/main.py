from datetime import datetime
import argparse
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

from dotenv import load_dotenv

from app.config import config
from app.reports.csv import report_csv_append
from app.reports.webhook import RequestTypes
from app.statistics.clubs.scrape import ResponseHandling
from app.validate_parameters import check_gym_ids, check_webhook

load_dotenv(ROOT_DIR / "vars.env")



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
