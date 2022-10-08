import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels.tsa.stattools as ts
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from itertools import product
from sklearn.metrics import mean_squared_error
from math import sqrt
import pmdarima as pm

#
dir_path = os.path.dirname(os.path.realpath(__file__))
data = pd.read_csv(f"{dir_path}/data/Dataset/trainset.csv", parse_dates=['date'], index_col='date')
#
print(data.head())
#
# # # Data denoise (U also can use the individual alphas)
alpha = 0.1
data.iloc[:,:8]= data.iloc[:,:8].ewm(alpha= alpha).mean()
# data.to_csv(f"{dir_path}/data/Dataset/train_filtered.csv")
#
#
#
# Run adfuller test to check for non-stationarity: ACF & PACF both assume stationarity
# def adf_test(timeseries):
#     print ('Results of Dickey-Fuller Test:')
#     dftest = ts.adfuller(timeseries, autolag='AIC')
#     dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
#     for key,value in dftest[4].items():
#         dfoutput['Critical Value (%s)'%key] = value
#     print (dfoutput)

# Found that the features and flow is stationary
# for name in data.columns.values[1:]:
#     adf_test(data[name].dropna())

# Look at the ACF & PACF
# f = plt.figure(figsize=(10,8))
# ax1 = f.add_subplot(211)
# plot_pacf(data[1000:2000].rainfall_Marborough,method = "ols",ax=ax1,lags=15)
# plt.grid()
# ax2 = f.add_subplot(212)
# plot_acf(data[1000:2000].rainfall_Marborough,ax=ax2,lags=15,)
# plt.grid()
# plt.show()

# grid search

# model = pm.auto_arima(data.rainfall_Marborough.values, start_p=1, start_q=1,
#                       test='adf',       # use adftest to find optimal 'd'
#                       max_p=3, max_q=3, # maximum p and q
#                       m=1,              # frequency of series
#                       d=None,           # let model determine 'd'
#                       seasonal=False,   # No Seasonality
#                       start_P=0,
#                       D=0,
#                       trace=True,
#                       error_action='ignore',
#                       suppress_warnings=True,
#                       stepwise=True)
#
# print(model.summary())

print(data.index)
data.index = pd.DatetimeIndex(data.index.values,
                               freq=data.index.inferred_freq)
training_mod = sm.tsa.SARIMAX(data.rainfall_Marborough.loc[:'1999-12-31'], order=(3,0,1))
training_res = training_mod.fit()

mod = sm.tsa.SARIMAX(data.rainfall_Marborough, order=(3,0,1))
res = mod.filter(training_res.params)

data['predict_Marborough'] = res.predict()
plt.title("")
data.rainfall_Marborough.loc['2000-01-01':'2000-12-31'].plot(label="original")
data.predict_Marborough.loc['2000-01-01':'2000-12-31'].plot(label="estimates")
plt.show()

# data.to_csv(f"{dir_path}/data/Dataset/train_filtered.csv",index=False)
# data.loc['2000-01-01':'2001-01-01'].plot(y=['predict',"rainfall_Ower"])
# plt.show()
# # forecast_error = data.rainfall_Ower.loc['2000-01-01':] - data.predict.loc['2000-01-01':]
# #
# # print(np.sqrt(np.sum(forecast_error**2) / T))
# print(res.summary())