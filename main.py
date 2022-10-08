import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sn
import dcor
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.ensemble import RandomForestRegressor
dir_path = os.path.dirname(os.path.realpath(__file__))
if __name__ =='__main__':
    df = pd.read_csv(f"{dir_path}/data/data_v2.csv")
    df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d')
    print(df.columns)
    # # Feature selection(data_v2.csv is after selection)
    # f = plt.figure(figsize=(19, 15))
    # mtrx = df.corr()
    # plt.matshow(mtrx, fignum=f.number)
    # plt.xticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14,
    #            rotation=45)
    # plt.yticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14)
    # cb = plt.colorbar()
    # cb.ax.tick_params(labelsize=14)
    # plt.title('Correlation Matrix', fontsize=16)
    # sn.heatmap(mtrx, cmap="Blues", annot=True)
    # plt.show()

    # Data denoise (U also can use the individual alphas)
    # alpha = 0.9
    # df.iloc[:,1:9]=df.iloc[:,1:9].ewm(alpha= alpha).mean()


    # ARMMA modelling to get feature lags example:














