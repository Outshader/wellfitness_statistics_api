
from clubs import club_addresses
import csv

def report_csv_append(ppl_count: int, timestamp: str, gyms: list) -> int:
    with open("logs.csv", "a", newline="", encoding="utf-8") as file:
        fieldnames = ["Club name", "date_time", "ppl_count"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for i in gyms:
            club_name = club_addresses[i]
            writer.writerow({
                "Club name": club_name, 
                "date_time": timestamp, 
                "ppl_count": ppl_count[club_name]
            })
        
    return 0