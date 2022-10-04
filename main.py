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
    df = pd.read_csv(f"{dir_path}/data/data3.csv")
    df = df[:1200]
    print(df.columns)
    # # plot
    # rain = df.filter(regex=r'tas|flow')
    #
    # #
    # f = plt.figure(figsize=(19, 15))
    # mtrx = rain.corr(method='spearman')
    # plt.matshow(mtrx, fignum=f.number)
    # plt.xticks(range(rain.select_dtypes(['number']).shape[1]), rain.select_dtypes(['number']).columns, fontsize=14,
    #            rotation=45)
    # plt.yticks(range(rain.select_dtypes(['number']).shape[1]), rain.select_dtypes(['number']).columns, fontsize=14)
    # cb = plt.colorbar()
    # cb.ax.tick_params(labelsize=14)
    # plt.title('Correlation Matrix', fontsize=16)
    # sn.heatmap(mtrx, cmap="Blues", annot=True)
    # plt.show()





    # print(harewood_ower)
    # print(df['rainfall_Andover'].corr(df['flow_BL']))
    # print(dcor.distance_correlation(df['rainfall_Andover'][:10000],df['flow_BL'][1:10001]))

    df.plot(x= 'date', y = ['rainfall_Quidhampton', 'flow_BL'])
    plt.show()  # Depending on whether you use IPython or interactive mode, etc.









