
# This file is to conduct steps to extract flow data: fill the missing flow data using external data from
# national river flow archive: https://nrfa.ceh.ac.uk/
import pandas as pd
import os
import matplotlib.pyplot as plt
import math
from statistics import mean
from sklearn.metrics import r2_score,mean_squared_error
data_path = os.path.dirname(os.path.realpath(__file__))+"/data"
plot_path = os.path.dirname(os.path.realpath(__file__))+"/plots"


# river flow at broadlands(data source: https://nrfa.ceh.ac.uk/)
broadlands = pd.read_csv(os.path.join(data_path,"broadlands.csv"))[19:]
broadlands.columns =["date","value","nothing"]
# broadlands.drop(["nothing"],axis=1,inplace=True)
broadlands.set_index("date",inplace=True)
broadlands_comp= broadlands.loc["2018-04-05":"2021-08-16"]

# river flow at testwood
testwood = pd.read_csv(os.path.join(data_path,"testwood.csv"),index_col=0)
testwood_comp= testwood.loc["2018-04-05":"2021-08-16"]


# river flow at conagar
conagar = pd.read_csv(os.path.join(data_path,"conagar.csv"),index_col=0)
conagar_comp = conagar.loc["2018-04-05":"2021-08-16"]

# riverflow at m27
m27 = pd.read_csv(os.path.join(data_path,"m27tv1.csv"),index_col=0)
m27_comp = m27.loc["2018-04-05":"2021-08-16"]

# river flow at ower
ower = pd.read_csv(os.path.join(data_path,"ower.csv"),index_col=0)
ower_comp = ower.loc["2018-04-05":"2021-08-16"]

frames = {'m27':m27_comp['value'],'conagar':conagar_comp['value'],'testwood':testwood_comp['value']}
result = pd.DataFrame(frames)
result['sum'] = result['m27']+result['conagar']+result['testwood']
result['broadlands'] = broadlands_comp['value'].astype(float)


# System identification: from broadland to the sum of the divisions
r = result[:77]
r.fillna(method="ffill",inplace=True)
r.plot(y=['sum','broadlands'])
SI = math.sqrt(mean_squared_error(r['sum'],r['broadlands']))/mean(r['sum'])*100
r2 = r2_score(r['sum'],r['broadlands'])
print(f"{SI:.2f}%",r2)
plt.title("Flow at Broadlands Vs Total flow at (Ower+Conagar+Testwood)")
plt.xlabel("Date(daily)")
plt.ylabel("Flow rate(m3/sec)")
plt.savefig(f"{plot_path}/flow.png")
plt.show()

# save the sum as input and broadland flow as output for system identification
dir_path = os.path.dirname(os.path.realpath(__file__))
result.to_csv(f"{data_path}/result.csv", index=False)


pred = pd.read_csv(os.path.join(data_path,"pred.csv"))

# print(pred[310:])
# print(r['sum'])
SI = math.sqrt(mean_squared_error(r['sum'],pred[:77]))/mean(r['sum'])*100
r2 = r2_score(r['sum'],pred[:77])
print(f"{SI:.2f}%",r2)

