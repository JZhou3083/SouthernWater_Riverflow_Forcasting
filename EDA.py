
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
r = result[310:]
r.fillna(method="ffill",inplace=True)
SI = math.sqrt(mean_squared_error(r['sum'],r['broadlands']))/mean(r['sum'])*100
r2 = r2_score(r['sum'],r['broadlands'])
print(f"{SI:.2f}%",r2)

# save the sum as input and broadland flow as output for system identification
dir_path = os.path.dirname(os.path.realpath(__file__))
result.to_csv(f"{data_path}/result.csv", index=False)


#
# plt.scatter(r['broadlands'],r['sum'])
# plt.xlabel("Broadlands GS")
# plt.ylabel("Sum of Conagar,m27 and Testwood GS")
# plt.text(10, 25, '$R2 = 0.92$', fontsize = 12)
# plt.savefig(f"{plot_path}/broadVsum.png")

# plt.figure(figsize=(3, 4))
# r.plot(y=['sum','broadlands'],x_compat=True)
# plt.xlabel("Date")
# plt.ylabel("Flow rate(m3/sec)")
# plt.savefig(f"{plot_path}/flow.png")


f, axarr = plt.subplots(1,2)
f.suptitle('Broadlands GS Vs Conagar+Testwood+M27 GSs')
r.plot(ax=axarr[0],y=['sum','broadlands'],x_compat=True)
axarr[0].set_ylabel("Flow rate(m3/sec)")
axarr[1].scatter(r['broadlands'],r['sum'])
axarr[1].set_xlabel("Broadlands GS")
axarr[1].set_ylabel("Sum ")
axarr[1].text(10, 25, '$R2 = 0.92$', fontsize = 10)
plt.savefig(f"{plot_path}/compare.png")
plt.show()


