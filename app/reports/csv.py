
import csv
from datetime import datetime

from app.scripts.csv import check_headers
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]



def report_csv_append(gym_data: dict[str, int], timestamp: str) -> None:
    fieldnames = ["Club address", "ppl_count", "timestamp"]
    check_headers(fieldnames)
    data_path = ROOT_DIR / "data" / "logs.csv"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    with open(data_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)        
        for address,count in gym_data.items():
            writer.writerow({
                "Club address": address, 
                "ppl_count": count,
                "timestamp": timestamp
            })


if __name__ == "__main__":
    report_csv_append({"asdf": 12}, datetime.now().strftime("%Y-%m-%d_%H-%M"))