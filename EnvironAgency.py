import requests
import logging as log
from datetime import date
station_ids = {"Ower":"151817001", "M27TV1":"151816012","Conagar":"151816005","Testwood":"151816003"}

class ImportFromEA:
    """This class will get data from environment agency"""
    def __init__(self):
        pass
    def get_flow_from(self, station="Ower", timeout = 10):
        # open url and get return data
        weblink = 'http://environment.data.gov.uk/hydrology'
        station_id = station_ids[station]
        url = f"{weblink}/data/readings.json?station.wiskiID={station_id}&observationType=Qualified"
        r = requests.get(url,timeout = timeout)
        if r.status_code != 200:
            log.error("Data fetching failed!")
        print(f"Fetched {station} GS's flow! ")
        data = r.json()
        return data['items']



if __name__== "__main__":
    print("Hello world!")
