
from clubs import club_addresses
import csv

def report_csv_append(gym_data: dict[str, int], timestamp: str) -> None:
    with open("logs.csv", "a", newline="", encoding="utf-8") as file:
        fieldnames = ["Club address", "date_time", "ppl_count"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for address,count in gym_data.items():
            writer.writerow({
                "Club address": address, 
                "date_time": timestamp, 
                "ppl_count": count
            })
