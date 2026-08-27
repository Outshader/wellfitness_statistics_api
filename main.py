from datetime import datetime
from api import Clubs
from config import Config
from reports import ReportCSV, ReportWebhook




    
    
class Main():
    def __init__(self):
        self.gym_ids = Config().gym_ids
    
    def main(self) -> None:
        gym_data = Clubs().clubs_main(self.gym_ids)
        print(gym_data)
        timestamp = datetime.now().isoformat()
        
        print("Logging results")
        
        print(gym_data, timestamp)
        
        if Config().skip_csv:
            print("Skipped csv append")
        else:
            ReportCSV().report_csv_append(gym_data, timestamp)
        
        if Config().skip_webhook:
            print("Skipped webhook")
        else:
            ReportWebhook().report_success(gym_data)
        print("Subtracting class data")
        # class_data_main()
        
        print("Done!")
        
if __name__ == "__main__":
    Main().main()