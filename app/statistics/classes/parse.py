
import csv
from datetime import datetime, timedelta
from pathlib import Path

from app.scripts.csv import check_headers
from app.statistics.classes.scrape import scrape_data

ROOT_DIR = Path(__file__).resolve().parents[3]


    
def iter_class(class_data):
    for data in class_data.get("CalendarData", []):
        for hourClass in data.get("ClassesPerHour", []):
            for dayClass in hourClass.get("ClassesPerDay", []):
                yield from dayClass
                
def pack_class_data(data: dict) -> list[dict]:       
    class_info = []
    for object in iter_class(data):
        Id = object["Id"]
        duration = object["Duration"]
        starttime = object["StartTime"]
        ppl_count = object["BookingIndicator"]["Indicator"]
        class_info.append({
            "Id": str(Id),
            "Duration": str(duration),
            "StartTime": str(starttime),
            "ppl_count": str(ppl_count)
        })  
    return class_info
    



    
def missing(data, id):
    for i in data:
        if i["Id"] == id:
            return False
        
        
def get_ppl_count(data, rows, ids):
    counts = {obj["Id"]: obj["ppl_count"] for obj in data if obj["Id"] in ids}
    for row in rows:
        count = row["Id"]
        counts[count] = max(counts.get(count, "0"), row["ppl_count"])
        

    return counts
         
            
def parse_duration(duration):
    duration = duration.strip("PT")
    
    hours = duration.split("H")[0] if "H" in duration else 0
    minutes = duration.split("H")[-1].strip("M")
    
    return timedelta(hours=int(hours), minutes=int(minutes))   
            
                
def subtract_ppl_count(to_subtract):
    data_logs = ROOT_DIR / "data" / "logs.csv"
    with open(data_logs, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    print(rows)
        
        
    for row in rows:
        log_time = datetime.fromisoformat(row["timestamp"])
        ppl_count = int(row["ppl_count"])
        for subtract in to_subtract:
            start_time = datetime.fromisoformat(subtract["StartTime"])
            duration = parse_duration(subtract["Duration"])
            end_time = start_time + duration
            
            if start_time <= log_time <= end_time:
                ppl_count -= int(subtract["ppl_count"])
        
        row["ppl_count"] = ppl_count
        
    logs_actual = ROOT_DIR / "data" / "logs_actual.csv"
    logs_actual.parent.mkdir(parents=True, exist_ok=True)
    with open(logs_actual, "w", newline="", encoding="utf-8") as file:
        fieldnames=["Club address", "timestamp", "ppl_count"]
        check_headers(fieldnames)
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
        
        
        
                

def verify_class_data(data):
    classes_file = ROOT_DIR / "data" / "classes.csv"

    with open(classes_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    now = datetime.now()

    to_subtract = []
    for row in rows:
        if datetime.fromisoformat(row["StartTime"]) <= now:
            to_subtract.append(
                {
                    "Id": row["Id"],
                    "ppl_count": None,
                    "Duration": row["Duration"],
                    "StartTime": row["StartTime"],
                }
            )

    if not to_subtract:
        return

    ppl_counts = get_ppl_count(data, rows, to_subtract)

    for row in to_subtract:
        row["ppl_count"] = ppl_counts.get(row["Id"], 0)

    subtract_ppl_count(to_subtract)
        


        
def class_data_main():        
    class_data = scrape_data()

    packed_data = pack_class_data(class_data)
    verify_class_data(packed_data)

    with open(ROOT_DIR / "data" / "classes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Id", "Duration", "StartTime", "ppl_count"])
        writer.writeheader()
        writer.writerows(packed_data)
                    
    


    
if __name__ == "__main__":
    class_data_main()