from EnvironAgency import ImportFromEA
import pandas as pd
import os
if __name__ =='__main__':
    """
    Parameters 
    station options: default source: EA
    - Ower
    - M27TV1 
    - Conagar
    - Testwood
    - Broadlands (External data source: NRFA)
    """
    p = ImportFromEA()
    stationNames = ["Ower","M27TV1","Conagar","Testwood","Broadlands"]
    for station in stationNames:
        data = p.get_flow_from(station)
        # convert to dataframe
        df = pd.DataFrame(data)

        # save the flow
        dir_path = os.path.dirname(os.path.realpath(__file__))
        df.to_csv(f"{dir_path}/data/{station}.csv",index=False)



