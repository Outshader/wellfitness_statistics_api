import os
import json
from typing import Optional
import requests
from dotenv import load_dotenv
import csv
from datetime import datetime
from pathlib import Path
from config import Config
from methods import check_headers


class ReportCSV():
    def report_csv_append(self, gym_data: dict[str, int], timestamp: str) -> None:
        fieldnames = ["Club address", "timestamp", "ppl_count"]
        logs_path = "data/logs.csv"
            

        check_headers(fieldnames)
        
    
        
        with open(logs_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)        
            for address,count in gym_data.items():
                writer.writerow({
                    "Club address": address, 
                    "ppl_count": count,
                    "timestamp": timestamp
                })



class ReportWebhook():
    def __init__(self) -> None:
        load_dotenv("data/vars.env")
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    def send_webhook(self, content: str, file: Optional[str | list] = None) -> int:
        if Config().skip_webhook:
            return 0


        data = {"payload_json": json.dumps({"content": content, "username": "status_bot"})}

        # Handle attachment if provided
        if file:
            file_path = Path("data") / str(file)
            if file_path.exists():
                with open(file_path, "rb") as f:
                    files = {"file": (file_path.name, f)}
                    response = requests.post(self.WEBHOOK_URL, data=data, files=files)
                    return response.status_code
            else:
                print(f"Attachment {file_path} not found; sending message without attachment.")

        # Default: send without attachment
        response = requests.post(self.WEBHOOK_URL, data=data)
        return response.status_code
                    

    def report_success(self, gym_data: dict[str,int]) -> int:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        message = "\n".join(f"{v} people at {k} at {timestamp}" for k,v in gym_data.items())
        if len(gym_data) == 1:
            return ReportWebhook().send_webhook(f"Successfully logged: {message}")
        else:
            return ReportWebhook().send_webhook(f"Successfully logged: \n{message}")

    def report_other_error_occured(self, log_file: Optional[str]) -> int:
        return ReportWebhook().send_webhook(
            "Some exception or error occured, check attached logs", log_file
        )
