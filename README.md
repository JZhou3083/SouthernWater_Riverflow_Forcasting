
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
shows the recent flow data of River Test, one of main source of water in Southampton: 

![River Test flow graph](https://www.southernwater.co.uk/media/7398/testriverflowmld.jpg)

In July, Southern Water introduced a 'Temporary Use Ban(TUB)' to all its customers in Hampshire and the Isle of Wight, restricting the unnecessary water usage such as watering a garden using a hosepipe. 

This project thereby aims to conduct time series analysis on the flow readings of River Test by the gauging stations, and construct a predictive model. The main objectives of the project include:
1. Analyse the flow of River Test using gauged data from Southern Water 
2. Construct a model that predicts river flow from climatic data, external data source will be utilized if needed
3. Validate the model and automate the data collecting and prediction using APIs
4. Make an APP for better UI

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Data Preparation
Collecting the data is a major task as hydrology data often suffers from discontinuity. The goal of this step is to collect at least 20 years of data for modelling.

### Flow data

The schematic of the hydrology of the River Test downstream of Romsey, adopted from Environment Agency in 2011 from Environment Agency: 

![Hydrology map of River Test gauge stations](https://github.com/JZhou3083/SouthernWater_Riverflow_Forcasting/blob/main/plots/Hydrology%20map.jpg?raw=true)

According to [the draught permit application](https://www.southernwater.co.uk/media/7278/11-description_of_the_proposal-1.pdf) by Southern Water(section 2.3.3), Testwood Bridge GS does not exist. Hence, the actual HOF data is obtained by 
summing the readings of the following gauge stations: 
1. River Great Test at Testwood
2. River Blackwater at Ower
3. Broadlands Fish Carrier at M27 TV1
4. River Little test at Conagar Bridge

(The interfacing module to Environment Agency database is the class __ImportFromEA__ in __EnvironAgency.py__.) However, the Testwood GS station of EA has a severe data missing issue, containing data from Apr 2018- Aug 2021 only and in low quality (unchecked estimation). 
Filling missing values is essential because rejecting data can significantly decrease the dataset size and forecasting reliability.

To fill the gap, I imputed it with the flow readings of a Broadlands Gauging Station(GS) owned by [National River Flow Archive] (https://nrfa.ceh.ac.uk/data/search), which locates slightly upstream of Conagar Bridge GS and Test Back GS stations(look at the hydrology map for a clearer idea).
Given the proximity between the stations, it is possible to achieve the approximation. To validate my idea, I extract the data from all the stations: 

![compare](https://github.com/JZhou3083/SouthernWater_Riverflow_Forcasting/blob/main/plots/compare.png?raw=true)
Then I also compute the Scatter Index and the coefficient of determination R2-score between the two series (code can be found from *EDA.py*) and found that for the existing data, the SI and R2-score are around 0.1 and 0.91 respectively. This is an unexpected good approximation. The equations of SI: 

<img src="https://latex.codecogs.com/svg.image?SI&space;=&space;\frac{RMSE}{\overline{X}}=\frac{\sqrt{\frac{\sum_{x_i}^{N}(x_i-\hat{x_i})^2}{N}}}{\frac{\sum_{x_i}^{N}x_i}{N}}" title="https://latex.codecogs.com/svg.image?SI = \frac{RMSE}{\overline{X}}=\frac{\sqrt{\frac{\sum_{x_i}^{N}(x_i-\hat{x_i})^2}{N}}}{\frac{\sum_{x_i}^{N}x_i}{N}}" class="center"/>

and R2-score: 

<img src="https://latex.codecogs.com/svg.image?R^{2}&space;=&space;1-\frac{RSS}{TSS}\\&space;" title="https://latex.codecogs.com/svg.image?R^{2} = 1-\frac{RSS}{TSS}\\ " class="center"/>

where RSS is the sum of squares of residuals, TSS is the total sum of squares. To sumarize, the closer R2-score is to 1 and the SI is to 0, the better the estimation it is. 


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Data collection 
- [x] Data preprocessing
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

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

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
