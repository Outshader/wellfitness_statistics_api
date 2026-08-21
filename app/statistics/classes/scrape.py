import requests

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