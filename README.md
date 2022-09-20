# SouthernWater_Riverflow_Forecasting
## Introduction
Hands off Flow (HOF) if a measurement of the river flow that triggers warning of when water supply company may be breaching their licence condition for water abstraction on the river, 
for the preservation of plants and wildlife. In the past eight months, Southampton has experienced the driest months in 131 years due to an extreme shortage of rainfall. The below graph, from the website of Southern Water,
shows the recent flow data of River Test, one of the two major river supplying water consuming of Southampton during 2022: 

![River Test flow graph](https://www.southernwater.co.uk/media/7398/testriverflowmld.jpg)

In 2022, flows have already dropped below '60-day' trigger and the '35-day' trigger and reaching HOF(updated in August). Southern Water, the water supply company,
thereby, introduced a 'Temporary Use Ban(TUB)' to all customers in Hampshire and the Isle of Wight, which suggested restrictions on unnecessary water usage such as watering a garden using a hosepipe. 

This project, aims to investigate the flow of River Test using the data from the gauge stations of Southern Water, and construct a predictive model
on the river flow. The main objectives of the project include:
1. Analyse the flow of River Test using gauged data from Southern Water 
2. Construct a model that predicts river flow from climatic data
3. Validate the model and automate the data extraction and prediction using Requests library and APIs
4. Make an APP for better UI

## Data collection
### Flow data
Data collection is the most time-consuming task so far as I am aiming to collect 20 years of daily flow data for the modelling. 
According to [the draught permit application](https://www.southernwater.co.uk/media/7278/11-description_of_the_proposal-1.pdf) by Southern Water(section 2.3.3), the HOF of River Test is measured by summing the readings of the following gauge stations: 
1. River Great Test at Testwood
2. River Blackwater at Ower
3. Broadlands Fish Carrier at M27 TV1
4. River Little test at Conagar Bridge

The schematic of the hydrology of the River Test downstream of Romsey, adopted from Environment Agency in 2011, can be found from Figure 2 of the application: 

![Hydrology map of River Test gauge stations](https://github.com/JZhou3083/SouthernWater_Riverflow_Forcasting/blob/main/plots/Hydrology%20map.jpg?raw=true)

The fact that HOF calculation is using Testwood GS combined with Ower GS station over Testwood Bridge GS is because Testwood Bridge GS does not exist yet. The interfacing module to Environment Agency 
database is class __ImportFromEA__ in __EnvironAgency.py__. However, the Testwood GS station of EA has a severe data missing, only containing data from Apr 2018 until Aug 2021 and in low quality (unchecked estimation). 
In order to fill the missing data, I used the data of [National River Flow Archive] (https://nrfa.ceh.ac.uk/data/search), who has Broadlands GS station that locates at the upstream of Testwood GS, Conagar Bridge GS and Test Back GS stations(look at the hydrology map above).
Hence, it is possible to estimate the sum of the stations' missing data from the readings of Broadlands GS station, which is a system identification task in theory. To validate my idea, I extract the data from all the stations and plot them out: 

![Broadlands Vs Sum]()


[//]: # (## Objectives)

[//]: # (The objective of the project are step-wise:)

[//]: # (1. Data collection and visualization. One of the biggest issue if the incomplete data of flow rate. I will first extract the flow data from [Environment Agency]&#40;https://environment.data.gov.uk/&#41;. Initial investigation on the flow will be conducted, followed by rainfall and temperature data collecting from external resource if neccessary&#40;[met office]&#40;https://www.metoffice.gov.uk/research/climate/maps-and-data/data/index&#41; etc.&#41;)

[//]: # (2. Data quality. Investigating further the data to check the given information. )

[//]: # (3. Data cleansing. )

[//]: # (4. Exploratory Data Analysis)

[//]: # (5. Feature Engineering )

[//]: # (6. Modelling)

[//]: # (7. Store the model and write up a script that $GET$ data from online and predict the flow rate on a daily basis. )

