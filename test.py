import requests, json
response = requests.post(
    url="https://wellfitness.perfectgym.com/ClientPortal2/Classes/ClassCalendar/WeeklyClasses",
    json={"clubId": 17, "daysInWeek": 0, "timeTableId": None},
    headers={
        "accept": "application/json",
        "x-requested-with": "XMLHttpRequest",
        "cp-lang": "pl",
        "cp-mode": "desktop"
    }
)
print(json.dumps(response.json(), indent=2))


