# SouthernWater_Riverflow_Forecasting
## Introduction
Hands off Flow (HOF) if a measurement of the river flow that triggers warning of when water supply company may be breaching their licence condition for water abstraction on the river, 
for the preservation of plants and wildlife. In the past eight months, Southampton has experienced the driest months in 131 years due to an extreme shortage of rainfall. The below graph, from the website of Southern Water,
shows the recent flow data of River Test, one of the two major river supplying water consuming of Southampton during 2022: 
![River Test flow graph](https://www.southernwater.co.uk/media/7398/testriverflowmld.jpg).
In 2022, flows have already dropped below '60-day' trigger and the '35-dat' trigger and reaching HOF(updated in July). Southern Water, the water supply company,
thereby, introduced a 'Temporary Use Ban(TUB)' to all customers in Hampshire and the Isle of Wight, which suggested restrictions on unnecessary water usage such as watering a garden using a hosepipe. 

This project, aims to investigate the flow of River Test using the data from the gauge stations of Southern Water, and construct a predictive model
on the river flow. The main objectives of the project include:
1. Analyse the flow of River Test from the gauge data
2. Construct a model that predicts river flow from climatic data
3. Validate the model and automate the data extraction and prediction making on a regular basis
4. Make an APP for user interfacing

## Data collection
Data collection is the most time-consuming task(so far). According to [the draught application](https://www.southernwater.co.uk/media/7278/11-description_of_the_proposal-1.pdf)(section 2.3.3), the HOF of River Test is measured by summing the readings of the following gauge stations: 
1. River Great Test at Testwood
2. River Blackwater at Ower
3. Broadlands Fish Carrier at M27 TV1
4. River Little test at Conagar Bridge

The schematic of the hydrology of the River Test downstream of Romsey, adopted from Environment Agency in 2011, can be found from Figure 2 of the application: 



[//]: # (## Objectives)

[//]: # (The objective of the project are step-wise:)

[//]: # (1. Data collection and visualization. One of the biggest issue if the incomplete data of flow rate. I will first extract the flow data from [Environment Agency]&#40;https://environment.data.gov.uk/&#41;. Initial investigation on the flow will be conducted, followed by rainfall and temperature data collecting from external resource if neccessary&#40;[met office]&#40;https://www.metoffice.gov.uk/research/climate/maps-and-data/data/index&#41; etc.&#41;)

[//]: # (2. Data quality. Investigating further the data to check the given information. )

[//]: # (3. Data cleansing. )

[//]: # (4. Exploratory Data Analysis)

[//]: # (5. Feature Engineering )

[//]: # (6. Modelling)

[//]: # (7. Store the model and write up a script that $GET$ data from online and predict the flow rate on a daily basis. )

