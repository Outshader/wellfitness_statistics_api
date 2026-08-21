import os
import json
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT_DIR = Path(__file__).resolve().parents[2]

import requests
from dotenv import load_dotenv

from app.validate_parameters import check_webhook





class SendRequest():
    def __init__(self) -> None:
        load_dotenv(ROOT_DIR / "vars.env")
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    def send_webhook(self, content: str, file: Optional[str | list] = None) -> int:
        data = {"payload_json": json.dumps({"content":content, "username":"status_bot"})}

        if file and Path(file).exists():
            with open(file, "rb") as f:
                files = {"file": (Path(file).name, f)}
                response = requests.post(self.WEBHOOK_URL, data=data, files=files)
                return response.status_code
        else:
            response = requests.post(self.WEBHOOK_URL, data=data)
            return response.status_code
                    

    def create_debug_zip(self, txt: str, txt_split: str, filename: str) -> str:
        temp_dir = tempfile.mkdtemp()
        print(f"Created temp dir {temp_dir}")
        screenshot_filename = filename + ".png"

        if Path(screenshot_filename).exists():
            shutil.copy(screenshot_filename, temp_dir)
            print(f"Copied {screenshot_filename} to {temp_dir}")

        with open(Path(temp_dir) / "full_text.txt", 'w') as file:
            file.write("\n".join(txt))

        with open(Path(temp_dir) / "split_text.txt", 'w') as file:
            file.write("\n".join(txt_split))
            
        print(f"Created full_text.txt and split_text.txt")
        
        current_time = filename
        zip_name = shutil.make_archive(f"{current_time}_log", "zip", temp_dir)
                    
        print(f"Archived to {zip_name}")
        shutil.rmtree(temp_dir)
        return zip_name


class RequestTypes():
    def __init__(self):
        if not check_webhook():
            raise RuntimeError("Missing Webhook!")
        
        
    def report_success(self, gym_data: dict[str,int]) -> int:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        message = "\n".join(f"{v} people at {k} at {timestamp}" for k,v in gym_data.items())
        if len(gym_data) == 1:
            return SendRequest().send_webhook(f"Successfully logged: {message}")
        else:
            return SendRequest().send_webhook(f"Successfully logged: \n{message}")

    def report_other_error_occured(self, log_file: Optional[str]) -> int:
        return SendRequest().send_webhook("Some exception or error occured, check attached logs", log_file)

    def report_ppl_count_not_found(self, txt: str, txt_split: str, filename: str) -> int:
        return SendRequest().send_webhook("The gym rat counter is down!", [txt, txt_split, filename])


