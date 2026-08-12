import requests
import shutil
import tempfile
from datetime import datetime
import os
import json
from typing import Optional
from dotenv import load_dotenv
from check_valid_parameters import check_webhook





class send_request():
    def __init__(self):
        load_dotenv("vars.env")
        WEBHOOK_URL = os.getenv("WEBHOOK_URL")
        

    def send_webhook(self, content: str, file: Optional[str | list] = None) -> int:
        data = {"payload_json": json.dumps({"content":content, "username":"status_bot"})}
        

        
        if file and os.path.exists(file):
            with open(file, "rb") as f:  
                files = {"file": (os.path.basename(file), f)}
                response = requests.post(self.WEBHOOK_URL, data=data, files=files)
                return response.status_code
            
        else:
            response = requests.post(self.WEBHOOK_URL, data=data)
            return response.status_code
                    

    def create_debug_zip(txt: str, txt_split: str, filename: str) -> str:
        temp_dir = tempfile.mkdtemp()
        print(f"Created temp dir {temp_dir}")
        screenshot_filename = filename + ".png"
        
        if os.path.exists(screenshot_filename):
            shutil.copy(screenshot_filename, temp_dir)
            print(f"Copied {screenshot_filename} to {temp_dir}")
        
        with open(os.path.join(temp_dir, "full_text.txt"), 'w') as file:
            file.write("\n".join(txt))
            
        with open(os.path.join(temp_dir, "split_text.txt"), 'w') as file:
            file.write("\n".join(txt_split))
            
        print(f"Created full_text.txt and split_text.txt")
        
        current_time = filename
        zip_name = shutil.make_archive(f"{current_time}_log", "zip", temp_dir)
                    
        print(f"Archived to {zip_name}")
        shutil.rmtree(temp_dir)
        return zip_name


class request_types():
    def __init__(self):
        if not check_webhook():
            raise RuntimeError("Missing Webhook!")
        
        
    def report_success(ppl_count: str) -> int:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        content = "\n".join(f"{k} {v}" for k,v in ppl_count.items())
        send = send_request()
        return send.send_webhook(f"Successfully logged: \n {content} \n people at {timestamp}")

    def report_other_error_occured(log_file: Optional[str]) -> int:
        send = send_request()
        return send.send_webhook("Some exception or error occured, check attached logs", log_file)

    def report_ppl_count_not_found(txt: str, txt_split: str, filename: str) -> int:
        send = send_request()
        return send.send_webhook("The gym rat counter is down!", [txt, txt_split, filename])


if __name__ == "__main__":
    types = request_types()
    txt, txt_split, filename, log_file, ppl_count = "", "", "", "", "0"
    request_types.report_ppl_count_not_found(txt, txt_split, filename)
    request_types.report_success(ppl_count)
    request_types.report_other_error_occured(log_file)
