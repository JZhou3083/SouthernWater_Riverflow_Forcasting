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

    # Data denoise
    f = plt.figure(figsize=(19, 15))
    for_plot = df[:1000]
    for_plot.plot(x='date',y='rainfall_Marborough')
    plt.show()











