import requests
import json
import csv
from datetime import datetime, timedelta
import shutil
from csv_methods import check_headers

def scrape_data():
    response = requests.post(
        url="https://wellfitness.perfectgym.com/ClientPortal2/Classes/ClassCalendar/WeeklyClasses",
        json={"clubId": 17, "categoryId": None, "timeTableId": None, "trainerId": None, "daysInWeek": 2, "QueryStartDate": "2026-08-17"},
        headers={
            "accept": "application/json",
            "x-requested-with": "XMLHttpRequest",
            "cp-lang": "pl",
            "cp-mode": "desktop"
        }
    )
    return response.json()
    
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
    


def write_contents(filename, content):
    fieldnames = ["Id", "Duration", "StartTime", "ppl_count"]
    with open(f"{filename}", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(content)
    
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
    hours = 0
    minutes = 0

    for i, val in enumerate(duration):
        if not val.isnumeric():
            continue

        if i + 1 < len(duration) and duration[i + 1] == "H":
            hours = int(val)

        elif i + 1 < len(duration) and duration[i + 1] == "M":
            if i > 0 and duration[i - 1].isnumeric():
                minutes = int(duration[i - 1] + val)
            else:
                minutes = int(val)

    return timedelta(hours=hours, minutes=minutes)   
       
def subtract_ppl_count(to_subtract):
    with open("logs.csv", "r") as file:
        reader = csv.DictReader(file, fieldnames=["Club name","date_time","ppl_count"])
        rows = list(reader)[1:]
        
    for row in rows:
        log_time = datetime.fromisoformat(row["date_time"])
        ppl_count = int(row["ppl_count"])
        for subtract in to_subtract:
            start_time = datetime.fromisoformat(subtract["StartTime"])
            duration = parse_duration(subtract["Duration"])
            end_time = start_time + duration
            
            if start_time <= log_time <= end_time:
                ppl_count -= int(subtract["ppl_count"])
        
        row["ppl_count"] = ppl_count
        
    with open("logs_actual.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Club name","date_time","ppl_count"])
        writer.writeheader()
        writer.writerows(rows)
                
        
                
    # subtract all the values from logs.csv using the timestamp +/- the duration of the class
    
    
    

    # write_contents()

def verify_class_data(data):
    # analyze logs.csv, make logs_actual.csv where the class_data will be accounted for, 
    with open("classes.csv", "r") as file:
        writer = csv.DictReader(file)
        rows = list(writer)
        
    to_subtract = []
    ppl_count = []
    for row in rows:
        row_id = row["Id"]
        if datetime.fromisoformat(row["StartTime"]) <= datetime.now():
            to_subtract.append({"Id": row_id, "ppl_count": None, "Duration": row["Duration"], "StartTime": row["StartTime"]})
            ppl_count.append(row_id)
        elif missing(data, row["Id"]):
            to_subtract.append({"Id": row_id, "ppl_count": None, "Duration": row["Duration"], "StartTime": row["StartTime"]})
            ppl_count.append(row_id)
            
    if to_subtract:
        ppl_count = get_ppl_count(data, rows, to_subtract)
        for i in to_subtract:
            i["ppl_count"] = ppl_count.get(i["Id"], 0)
        subtract_ppl_count(to_subtract)
        

       
        
def class_data_main():        
    class_data = scrape_data()

    packed_data = pack_class_data(class_data)
    verify_class_data(packed_data)
    

        
    write_contents("classes.csv", packed_data)

                    
    


    
if __name__ == "__main__":
    class_data_main()