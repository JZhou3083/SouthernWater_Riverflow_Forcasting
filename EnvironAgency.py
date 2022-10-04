import requests
import logging as log
import json
import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
station_ids = {"Ower":"151817001", "M27TV1":"151816012","Conagar":"151816005","Testwood":"151816003","Broadlands":"42004"}
class ImportFromEA:
    """This class will get data from environment agency, return in json format"""
    def __init__(self):
        pass
    # Get daily river flow at unit m2/sec, data source: EA & NRFA
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

        # convert to retrieve data
        if station =="Broadlands":
            content = json.loads(r.content.decode())['data-stream']
            data = {"date":content[0::2],"value":content[1::2]}
        else:
            data = json.loads(r.content.decode())
            data = data["items"]
        return data

    def flow_to_csv(self, stationNames= ["Broadlands","Ower"]):
        """
        :param save_csv: save the data as csv
        :return: DataFrame of flow data from all stations
        """
        for station in stationNames:
            data = self.get_flow_from(station)
            # convert to dataframe
            df = pd.DataFrame(data)
            df['date']=pd.to_datetime(df['date'].astype(str), format='%Y/%m/%d')
            df = df[df.date>='1980/1/1']
            df = df[['date','value']]

            df.rename(columns={'value':f"flow_{station}"})
            df.sort_values('date', inplace=True) # Some dataset not sorted

            # save the flow
            df.to_csv(f"{dir_path}/data/flow_{station}.csv", index=False)



if __name__=='__main__':
    p = ImportFromEA()
    p.flow_to_csv()


