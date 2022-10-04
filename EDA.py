
# This file is to conduct steps to extract flow data: fill the missing flow data using external data from
# national river flow archive: https://nrfa.ceh.ac.uk/
import pandas as pd
import os
import matplotlib.pyplot as plt
import math
from statistics import mean
from sklearn.metrics import r2_score,mean_squared_error
data_path = os.path.dirname(os.path.realpath(__file__))+"/data/flow"
plot_path = os.path.dirname(os.path.realpath(__file__))+"/plots"
def crosscorr(datax, datay, lag=0):
    """ Lag-N cross correlation.
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length

    Returns
    ----------
    crosscorr : float
    """
    return datax.corr(datay.shift(lag))

# river flow at broadlands(data source: https://nrfa.ceh.ac.uk/)
broadlands = pd.read_csv(os.path.join(data_path,"broadlands.csv"))[19:]
broadlands.columns =["date","value"]
broadlands.sort_values(by="date",inplace=True)
broadlands.set_index("date",inplace=True)
broadlands_comp= broadlands.loc["2019-02-05":"2021-08-16"]
print(broadlands_comp)

# river flow at testwood
testwood = pd.read_csv(os.path.join(data_path,"testwood.csv"),index_col=0)
testwood.sort_values(by="date",inplace=True)
print(testwood)
testwood_comp= testwood.loc["2019-02-05":"2021-08-16"]

print(testwood_comp)



# river flow at conagar
conagar = pd.read_csv(os.path.join(data_path,"conagar.csv"),index_col=0)
conagar.sort_values(by="date",inplace=True)
conagar_comp = conagar.loc["2019-02-05":"2021-08-16"]


# riverflow at m27
m27 = pd.read_csv(os.path.join(data_path,"m27tv1.csv"),index_col=0)
m27.sort_values(by="date",inplace=True)
m27_comp = m27.loc["2019-02-05":"2021-08-16"]


# river flow at ower
ower = pd.read_csv(os.path.join(data_path,"ower.csv"),index_col=0)
ower.sort_values(by="date",inplace=True)
ower_comp = ower.loc["2019-02-05":"2021-08-16"]

print(ower_comp)
frames = {'m27':m27_comp['value'],'conagar':conagar_comp['value'],'testwood':testwood_comp['value']}
result = pd.DataFrame(frames)
result['sum'] = result['m27']+result['conagar']+result['testwood']
result['broadlands'] = broadlands_comp['value'].astype(float)

# System identification: from broadland to the sum of the divisions
r = result[310:]
print(r)
r.fillna(method="ffill",inplace=True)
SI = math.sqrt(mean_squared_error(r['sum'],r['broadlands']))/mean(r['sum'])*100
r2 = r2_score(r['sum'],r['broadlands'])
print(f"{SI:.2f}%",r2)

# save the sum as input and broadland flow as output for system identification
dir_path = os.path.dirname(os.path.realpath(__file__))
result.to_csv(f"{data_path}/result.csv", index=False)


#
plt.scatter(r['broadlands'],r['sum'])
plt.xlabel("Broadlands GS")
plt.ylabel("Sum of Conagar,m27 and Testwood GS")
plt.text(10, 25, '$R2 = 0.92$', fontsize = 12)
plt.savefig(f"{plot_path}/broadVsum.png")

plt.figure(figsize=(3, 4))
r.plot(y=['sum','broadlands'],x_compat=True)
plt.xlabel("Date")
plt.ylabel("Flow rate(m3/sec)")
plt.savefig(f"{plot_path}/flow.png")


# f, axarr = plt.subplots(1,2)
# f.suptitle('Broadlands GS Vs Conagar+Testwood+M27 GSs')
# r.plot(ax=axarr[0],y=['sum','broadlands'],x_compat=True)
# axarr[0].set_ylabel("Daily mean(m3/sec)")
# axarr[1].scatter(r['broadlands'],r['sum'])
# axarr[1].set_xlabel("Broadlands GS")
# axarr[1].set_ylabel("Sum ")
# axarr[1].text(10, 25, '$R2 = 0.92$', fontsize = 10)
# plt.savefig(f"{plot_path}/compare.png")
plt.show()

cov = [crosscorr(r['sum'], r['broadlands'], lag=i) for i in range(-7,7)]
plt.xlabel("days")
plt.title("correlation")
plt.stem(range(-7,7),cov)
plt.ylim(0,1)
plt.savefig(f"{plot_path}/cor.png")
plt.show()