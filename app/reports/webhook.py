import os
import json
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional


import requests
from dotenv import load_dotenv
from pathlib import Path
from app.config import config 

from app.validate_parameters import check_webhook


ROOT_DIR = Path(__file__).resolve().parents[3]


class SendRequest():
    def __init__(self) -> None:
        load_dotenv(ROOT_DIR / "vars.env")
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    def send_webhook(self, content: str, file: Optional[str | list] = None) -> int:
        if config().should_send_webhook():
            return 0


        data = {"payload_json": json.dumps({"content": content, "username": "status_bot"})}

        # Handle attachment if provided
        if file:
            file_path = ROOT_DIR / "data" / str(file)
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
                    




class RequestTypes():
    def report_success(self, gym_data: dict[str,int]) -> int:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        message = "\n".join(f"{v} people at {k} at {timestamp}" for k,v in gym_data.items())
        if len(gym_data) == 1:
            return SendRequest().send_webhook(f"Successfully logged: {message}")
        else:
            return SendRequest().send_webhook(f"Successfully logged: \n{message}")

    def report_other_error_occured(self, log_file: Optional[str]) -> int:
        return SendRequest().send_webhook("Some exception or error occured, check attached logs", log_file)


