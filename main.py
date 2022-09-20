from EnvironAgency import ImportFromEA
import pandas as pd
import os
if __name__ =='__main__':
    """
    station options: 
    Ower, M27TV1, Conagar
    
    """
    p = ImportFromEA()
    stationNames = ["Ower","M27TV1","Conagar","Testwood"]
    for station in stationNames:
        data = p.get_flow_from(station)
        # convert to dataframe
        df = pd.DataFrame(data)
        df= df.drop(['measure','dateTime'],axis=1).sort_values(by='date')
        df.rename(columns= {"value":f"flow_{station}"})

    # result = pd.merge(dfs[0], dfs[1], on="date", how="outer", validate="one_to_many")


        # save the flow
        dir_path = os.path.dirname(os.path.realpath(__file__))
        df.to_csv(f"{dir_path}/data/{station}.csv",index=False)
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # result.to_csv(f"{dir_path}/data/result.csv",index=False)

