import glob
from netCDF4 import num2date, Dataset
import pandas as pd
import numpy as np
import os
from calendar import monthrange
file_path = os.path.dirname(os.path.realpath(__file__))
stations_lookup = pd.read_csv(f"{file_path}/data/stations.csv")



class mergeFiles:
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    feature : str
        the data of interest- "rainfall", "tasmax"(daily max air temperature), "tasmin"(daily minimum air temperature)
    start_month : str
        the start month of interest
    end_month : str
        the end month of interest
    save_csv: BOOL
        save it as csv file or not

    Methods
    -------
    createDataFrame()
        create DataFrame of data

    fillData()
        read in data
    """

    def __init__(self, feature="rainfall",stations= stations_lookup[stations_lookup.type=='rain'].name.values.tolist(),save_csv=True):

        self.feature = feature
        self.df = None
        self.all_months = []
        self.save_csv = save_csv
        self.data_path =  f"{file_path}/data/CEDA"
        self.stations = stations

    def createDataFrame(self):
        """
        Build DataFrame for the data
        :return: DataFrame
        """
        # Record all the months of the netCDF files into a Python list self.all_months
        files = f"{self.data_path}/{self.feature}/*.nc"
        print(files)
        for file in glob.glob(files):
            print(file[-9:-3])
            data = Dataset(file, 'r')
            # print(time.units)
            month = file[-9:-3]
            self.all_months.append(month)
            data.close()

        # Creating an empty Pandas DataFrame covering the whole range of data
        mon_start = min(self.all_months)
        end_mon = max(self.all_months)

        date_range = pd.date_range(start=str(mon_start) + '01',
                                   end=str(end_mon) + '31',
                                   freq='D')
        self.df = pd.DataFrame(0.0, columns=[f"{self.feature}_{station}" for station in self.stations], index=date_range)

    def fillData(self):

        # Sorting the all_years python list
        self.all_months.sort()

        for mth in self.all_months:
            # Reading-in the data
            data = Dataset(f"{self.data_path}/{self.feature}/{mth}.nc", 'r')
            lats,lons = data.variables['latitude'][:],data.variables['longitude'][:] # Do it for every nc file just in case of difference

            # Accessing the average temparature data
            value = data.variables[self.feature]


            # Creating the date range for each year during each iteration
            start = str(mth) + '01'
            year = mth[:4]
            days_of_month = monthrange(int(year), int(mth[-2:]))[1]
            end = str(mth) + str(days_of_month)
            d_range = pd.date_range(start=start,
                            end=end,
                            freq='D')
            for station in self.stations:
                cord = (stations_lookup[stations_lookup.name==station].latitude.values, stations_lookup[stations_lookup.name==station].longitude.values)
                min_index_lat, min_index_lon = self.getclosest_ij(lats, lons, cord)
                for t_index in np.arange(0, len(d_range)):
                    print(f'Recording the {self.feature} value at {station} for: ' + str(d_range[t_index]))
                    self.df.loc[d_range[t_index]][f"{self.feature}_{station}"] = value[t_index, min_index_lat, min_index_lon]
            data.close()
        if self.save_csv:
            self.df.to_csv(f"{self.data_path}/{self.feature}.csv")
        return self.df

    def getclosest_ij(self,lats, lons, cords):
        """
        :param lats: latitude lookup  list
        :param lons: longitude lookup list
        :param cords: (latitude,longitude)
        :return: index_y, index_x of the (latitude, longitude)
        """
        latpt, lonpt = cords
        # find squared distance of every point on grid
        dist_sq = (lats - latpt) ** 2 + (lons - lonpt) ** 2
        # 1D index of minimum dist_sq element
        minindex_flattened = dist_sq.argmin()
        # Get 2D index for latvals and lonvals arrays from 1D index
        return np.unravel_index(minindex_flattened, lats.shape)



if __name__=='__main__':

    # rain
    rain = mergeFiles(feature="rainfall")
    rain.createDataFrame()
    df=rain.fillData()

    # maximum temperature
    tasmax = mergeFiles(feature="tasmax",stations=stations_lookup[stations_lookup.type=='temp'].name.values.tolist())
    tasmax.createDataFrame()
    df_tasmax = tasmax.fillData()

    # minimum temperature
    tasmin = mergeFiles(feature="tasmin",stations=stations_lookup[stations_lookup.type=='temp'].name.values.tolist())
    tasmin.createDataFrame()
    df_tasmin = tasmin.fillData()
