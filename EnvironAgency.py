import requests
import logging as log
import json
station_ids = {"Ower":"151817001", "M27TV1":"151816012","Conagar":"151816005","Testwood":"151816003","Broadlands":"42004"}

class ImportFromEA:
    """This class will get data from environment agency, return json format"""
    def __init__(self):
        pass
    def get_flow_from(self, station="Ower", timeout = 10):
        # open url and get return data
        station_id = station_ids[station]
        if station =="Broadlands":
            # get from NRFA database
            weblink = 'https://nrfaapps.ceh.ac.uk'
            url = f"{weblink}/nrfa/ws/time-series?format=json-object&data-type=gdf&station={station_id}"

        else:
            # get from EA database
            weblink = 'http://environment.data.gov.uk/hydrology'
            url = f"{weblink}/data/readings.json?station.wiskiID={station_id}&observationType=Qualified"
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            log.error("Data fetching failed!")
        else:
            print(f"Fetched {station} GS's flow! ")

        # data indifferent format
        if station =="Broadlands":
            content = json.loads(r.content.decode())['data-stream']
            data = {"date":content[0::2],"value":content[1::2]}
        else:
            data = json.loads(r.content.decode())
            data = data["items"]
        return data



if __name__== "__main__":
    print("Hello world!")
