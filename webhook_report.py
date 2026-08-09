import requests
import shutil
import tempfile
from datetime import datetime
import os
import json
from typing import Optional
from dotenv import load_dotenv
from check_valid_parameters import check_webhook


load_dotenv("vars.env")

webhook_url = os.getenv("webhook_url")

def send_webhook(content: str, file: Optional[str] = None) -> int:
    data = {"payload_json": json.dumps({"content":content, "username":"status_bot"})}
    if file and os.path.exists(file):
        with open(file, "rb") as f:  
            files = {"file": (os.path.basename(file), f)}
            response = requests.post(webhook_url, data=data, files=files)
            return response.status_code
    else:
        response = requests.post(webhook_url, data=data)
        return response.status_code
                

def create_debug_zip(txt: str, txt_split: str, filename: str):
    temp_dir = tempfile.mkdtemp()
    print(f"Created temp dir {temp_dir}")
    screenshot_filename = filename + ".png"
    
    if os.path.exists(screenshot_filename):
        shutil.copy(screenshot_filename, temp_dir)
        print(f"Copied {screenshot_filename} to {temp_dir}")
    
    with open(os.path.join(temp_dir, "full_text.txt"), 'w') as file:
        file.write("\n".join(txt_split))
        
    with open(os.path.join(temp_dir, "split_text.txt"), 'w') as file:
        file.write("\n".join(txt_split))
        
    print(f"Created full_text.txt and split_text.txt")
    
    current_time = filename
    zip_name = shutil.make_archive(f"{current_time}_log", "zip", temp_dir)
                
    print(f"Archived to {zip_name}")
    shutil.rmtree(temp_dir)
    return zip_name



def report_success(ppl_count: str) -> int:
    ppl_count = ppl_count
    return send_webhook(f"Successfully logged {ppl_count} people at {datetime.now().strftime('%Y-%m-%d_%H-%M')}")

def other_error_occured(log_file: str) -> int:
    return send_webhook("Some exception or error occured, check attached logs", log_file)

def ppl_count_not_found(txt: str, txt_split: str, filename: str) -> int:
    zip_name = create_debug_zip(txt, txt_split, filename)
    return send_webhook("The gym rat counter is down!", zip_name)

if __name__ == "__main__":
    txt, txt_split, filename, log_file, ppl_count = "", "", "", "", "0"
    ppl_count_not_found(txt, txt_split, filename)
    report_success(ppl_count)
    other_error_occured(log_file)
