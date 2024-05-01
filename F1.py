import requests
import datetime

def get_current_year():
    today = datetime.date.today()
    year = today.year
    return year
current_year = get_current_year()
URL = f"http://ergast.com/api/f1/{current_year}"
