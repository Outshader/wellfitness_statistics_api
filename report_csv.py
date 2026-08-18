
from clubs import club_addresses
import csv
from datetime import datetime
from csv_methods import check_headers





            
            
            

    
def report_csv_append(gym_data: dict[str, int], timestamp: str) -> None:
    fieldnames = ["Club address", "ppl_count", "timestamp"]
    check_headers(fieldnames)
    with open("logs.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for address,count in gym_data.items():
            writer.writerow({
                "Club address": address, 
                "ppl_count": count,
                "timestamp": timestamp
            })


if __name__ == "__main__":
    report_csv_append({"asdf": 12}, datetime.now().strftime("%Y-%m-%d_%H-%M"))