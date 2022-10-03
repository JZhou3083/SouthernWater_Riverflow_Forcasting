
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#Dta Preparation">Data Preparation</a>
      <ul>
        <li><a href="#Flow data">Flow data</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[//]: # ([![Product Name Screen Shot][product-screenshot]]&#40;https://example.com&#41;)

Hands off Flow (HOF) is a measurement of the river flow that triggers warning of when water supply company may be breaching their licence condition for water abstraction on the river to preserve water resource for plants and wildlife. 

In the past eight months, Southampton has experienced the driest months in 131 years due to an extreme shortage of rainfall. The below graph, from the website of Southern Water,
shows the recent flow data of River Test, one of main water source in Southampton: 
<p align="center">
<img src="/plots/testriverflowmld.jpg" height="300">
</p>

In July, Southern Water introduced a 'Temporary Use Ban(TUB)' to all its customers in Hampshire and the Isle of Wight, restricting the unnecessary water usage such as watering a garden using a hosepipe. 

This project thereby aims to conduct time series analysis on the flow readings of River Test by the gauging stations, and construct a predictive model. The main objectives of the project include:
1. Analyse the flow of River Test using gauged data from Southern Water 
2. Construct a model that predicts river flow from climatic data, external data source will be utilized if needed
3. Validate the model and automate the data collecting and prediction using APIs
4. Make an APP for better UI

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Methodlogy

The target of this work is to provide a reusable pipeline for water availability forecasting. It provides also a comparative analysis about different forecasting strategies and models. Every datasets are differents from each other, so each dataset will be treated independantly following a general pipeline. 
I am aiming for a mid and long term forecasting and do not intend to used inferred outputs for future prediction, therefore excluding the usage of recursive forecasting.  

The general methodology falls into three categories: 
* data preparation: Sourcing, imputing, cleansing and feature engineering for model feeding. 
* evaluation strategy: Expanding window cross validation 
* modeling strategy: Ensemble learning 


### Data preparation

Data collection is a difficult task as climatic data of EA often suffers from significant discontinuities. The target is to collect at least 20 years of data for modelling, for which I exploited external data sources extensively
if correlation analysis indicated good matching to the data of EA.

#### Daily Mean Flow (m3/s) 
The schematic of the hydrology of the River Test downstream of Romsey, adopted from Environment Agency in 2011 from Environment Agency(EA): 
<p align="center">
<img src="/plots/hydroMap.jpg"  width="300" height="300" class="center">
</p>

According to [the draught permit application](https://www.southernwater.co.uk/media/7278/11-description_of_the_proposal-1.pdf) by Southern Water(section 2.3.3), Testwood Bridge GS does not exist. Hence, the actual HOF data is obtained by 
summing the readings of the following gauge stations: 
1. River Great Test at Testwood
2. River Blackwater at Ower
3. Broadlands Fish Carrier at M27 TV1
4. River Little test at Conagar Bridge

(The interfacing module to Environment Agency database is the class __ImportFromEA__ in __EnvironAgency.py__). However, the Testwood GS station of EA has a severe data missing issue, containing data from Apr 2018- Aug 2021 only and in low quality (unchecked estimation). 
Filling missing values is essential because rejecting data can significantly decrease the dataset size and forecasting reliability.

To fill the gap, I imputed it with the flow readings of a Broadlands Gauging Station(GS) locating at slightly upstream of Conagar Bridge GS and Test Back GS stations(look at the hydrology map for a clearer idea), from National River Flow Archive([NRFA](https://nrfa.ceh.ac.uk/data/search)).
Given the proximity, it is possible to achieve the approximation or estimation(a system identification task). To validate my idea, I extract the data from all the stations:
<p align="center">
<img src="/plots/compare.png" width= "450" height="300">
</p>

Then I compute the Scatter Index and the coefficient of determination R2-score between the two series (code can be found from *EDA.py*) and found that for the existing data, the SI and R2-score are around 0.1 and 0.91 respectively. This is an unexpected good approximation. The equations of SI: 
<p align="center">
<img src="https://latex.codecogs.com/svg.image?SI&space;=&space;\frac{RMSE}{\overline{X}}=\frac{\sqrt{\frac{\sum_{x_i}^{N}(x_i-\hat{x_i})^2}{N}}}{\frac{\sum_{x_i}^{N}x_i}{N}}" title="https://latex.codecogs.com/svg.image?SI = \frac{RMSE}{\overline{X}}=\frac{\sqrt{\frac{\sum_{x_i}^{N}(x_i-\hat{x_i})^2}{N}}}{\frac{\sum_{x_i}^{N}x_i}{N}}"/>
</p>

and R2-score: 
<p align="center">
<img src="https://latex.codecogs.com/svg.image?R^{2}&space;=&space;1-\frac{RSS}{TSS}\\&space;" title="https://latex.codecogs.com/svg.image?R^{2} = 1-\frac{RSS}{TSS}\\ " class="center"/>
</p>

where RSS is the sum of squares of residuals, TSS is the total sum of squares. To sumarize, the closer R2-score is to 1 and the SI is to 0, the better the estimation it is. 
Considering there may be delay between the two data, I also ran correlation check on the two time series: 
<p align="center">
<img src="/plots/cor.png" width="400" height="300">
</p>

It is found that the greatest correlation lies on the day 0, which means readings between Broadlands GS and the sum of the other three has a negligible delay. 
I also built a transfer model(*data/tfModel.mat*) using system identification toolbox of MATLAB to achieve closer approximation, whereas the model overfits due to the shortage of training data. 
Finally, outputs of the model are:
1. Daily flow mean gauged at Broadlands GS from EA
2. Daily flow mean gauged at Ower GS from NRFA

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Precipitation

Rainfall data collection and imputation used the same methodology as flow but with the two extra tasks:
- Locations. It is assumed that rainfall and temperature at the upstream has impact on the river flow. The sampling point of the rainfall and temperature observations were chosen according to the collecting stations locaitons 
of EA but with interpolation, although high correlation of the locations is expected. Therefore, PCA will be conducted to in the data preprocessing. 
- Interpolation and extraction. The dataset I used was the [HadUK-Grid](https://data.ceda.ac.uk/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.1.0.0/5km) at the resolution of 5km national grid referenced data, in the netCDF format. 
The interface that merge netCDF files and extract data of interested coordinates is *merge_nc_files.py*. 

<!-- ROADMAP -->
## Roadmap

- [x] Data preparation
- [ ] Feature engineering  
- [ ] Modelling 
- [ ] Validation 
- [ ] APP 


See the [open issues](https://github.com/JZhou3083/SouthernWater_Riverflow_Forcasting/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>






<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Southernwater](https://www.southernwater.co.uk/)
* [National River Flow Archive](https://nrfa.ceh.ac.uk/)
* [A super Learner for water availability forecasting(R)](https://www.kaggle.com/code/vlarmet/a-super-learner-for-water-availability-forecasting)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
