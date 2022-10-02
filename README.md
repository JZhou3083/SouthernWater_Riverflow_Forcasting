
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
- Locations. It is nearly impossible to forecast daily precipitation with local data only. Therefore, I incorporate 
as flow but in NetCDF4 format. A tutorial on data analysis using Python and NetCDF4 can be found [here](http://fastml.com/predicting-solar-energy-from-weather-forecasts-plus-a-netcdf4-tutorial/).

<!DOCTYPE html>
<head>    
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    
        <script>
            L_NO_TOUCH = false;
            L_DISABLE_3D = false;
        </script>
    
    <style>html, body {width: 100%;height: 100%;margin: 0;padding: 0;}</style>
    <style>#map {position:absolute;top:0;bottom:0;right:0;left:0;}</style>
    <script src="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js"></script>
    <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>
    
            <meta name="viewport" content="width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
            <style>
                #map_d1ce6e21ca701dc4a08eafe35cda8b6c {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
            </style>
        
</head>
<body>    
    
            <div class="folium-map" id="map_d1ce6e21ca701dc4a08eafe35cda8b6c" ></div>
        
</body>
<script>    
    
            var map_d1ce6e21ca701dc4a08eafe35cda8b6c = L.map(
                "map_d1ce6e21ca701dc4a08eafe35cda8b6c",
                {
                    center: [51.0, -1.53],
                    crs: L.CRS.EPSG3857,
                    zoom: 9,
                    zoomControl: true,
                    preferCanvas: false,
                }
            );

            

        
    
            var tile_layer_887930e4320023aad07664b0a4e1f497 = L.tileLayer(
                "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                {"attribution": "Data by \u0026copy; \u003ca href=\"http://openstreetmap.org\"\u003eOpenStreetMap\u003c/a\u003e, under \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eODbL\u003c/a\u003e.", "detectRetina": false, "maxNativeZoom": 18, "maxZoom": 18, "minZoom": 0, "noWrap": false, "opacity": 1, "subdomains": "abc", "tms": false}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var marker_287b41d8022cd59fb093b454b4f26014 = L.marker(
                [50.95, -1.53],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_d5e893bf422081dd1cd0762bfa3a9fc2 = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_287b41d8022cd59fb093b454b4f26014.setIcon(icon_d5e893bf422081dd1cd0762bfa3a9fc2);
        
    
            marker_287b41d8022cd59fb093b454b4f26014.bindTooltip(
                `<div>
                     ('E13590', 50.95)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_3f33412a5d67a17a431fa334fad84ebb = L.marker(
                [50.99, -1.49],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_32bf8bbcde3d2b5e54c028e933104add = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_3f33412a5d67a17a431fa334fad84ebb.setIcon(icon_32bf8bbcde3d2b5e54c028e933104add);
        
    
            marker_3f33412a5d67a17a431fa334fad84ebb.bindTooltip(
                `<div>
                     ('E13560', 50.99)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_c64594fa1bf08f635dad08302eef49e3 = L.marker(
                [50.88, -1.56],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_b6b56f4292b7fca140d0891383932eb1 = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_c64594fa1bf08f635dad08302eef49e3.setIcon(icon_b6b56f4292b7fca140d0891383932eb1);
        
    
            marker_c64594fa1bf08f635dad08302eef49e3.bindTooltip(
                `<div>
                     ('E13600', 50.88)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_63517c59a90fb423b5492d5857f1ae96 = L.marker(
                [51.1, -1.56],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_5f551b5d0dd58b94f5d6f91a2a89fdb6 = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_63517c59a90fb423b5492d5857f1ae96.setIcon(icon_5f551b5d0dd58b94f5d6f91a2a89fdb6);
        
    
            marker_63517c59a90fb423b5492d5857f1ae96.bindTooltip(
                `<div>
                     ('E13580', 51.1)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_85dcc6cf02db7b6ab6982673be580001 = L.marker(
                [51.22, -1.47],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_4f9d05610b53945547eba0580a87ffe8 = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_85dcc6cf02db7b6ab6982673be580001.setIcon(icon_4f9d05610b53945547eba0580a87ffe8);
        
    
            marker_85dcc6cf02db7b6ab6982673be580001.bindTooltip(
                `<div>
                     ('E13980', 51.22)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_c7a407783f8c979f3b8b9b93753e051d = L.marker(
                [51.25, -1.26],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_f35774d35e6a510ddeda5207559d43ff = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_c7a407783f8c979f3b8b9b93753e051d.setIcon(icon_f35774d35e6a510ddeda5207559d43ff);
        
    
            marker_c7a407783f8c979f3b8b9b93753e051d.bindTooltip(
                `<div>
                     ('E11480', 51.25)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_0c7141195ad3dd05963d93faed129cf5 = L.marker(
                [51.25, -1.26],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_f8ac0b82f914a8f5c8cd18255ca3abc2 = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_0c7141195ad3dd05963d93faed129cf5.setIcon(icon_f8ac0b82f914a8f5c8cd18255ca3abc2);
        
    
            marker_0c7141195ad3dd05963d93faed129cf5.bindTooltip(
                `<div>
                     ('E14080', 51.25)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_b94b0dd74e2221ac85504085046966db = L.marker(
                [51.22, -1.67],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_d0562bf8f0fff2a53d4a5f5869a923ba = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_b94b0dd74e2221ac85504085046966db.setIcon(icon_d0562bf8f0fff2a53d4a5f5869a923ba);
        
    
            marker_b94b0dd74e2221ac85504085046966db.bindTooltip(
                `<div>
                     ('E43104', 51.22)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_1e9eb119c924b6604f738dff09beb3f2 = L.marker(
                [51.16, -1.89],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_c9d759da249e372c929e14047697bf1a = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_1e9eb119c924b6604f738dff09beb3f2.setIcon(icon_c9d759da249e372c929e14047697bf1a);
        
    
            marker_1e9eb119c924b6604f738dff09beb3f2.bindTooltip(
                `<div>
                     ('E43103', 51.16)
                 </div>`,
                {"sticky": true}
            );
        
    
            var marker_35f247d43f31b67f4ca4c81514576e19 = L.marker(
                [50.97, -1.92],
                {}
            ).addTo(map_d1ce6e21ca701dc4a08eafe35cda8b6c);
        
    
            var icon_481c26120acd2d02759670be6a02a902 = L.AwesomeMarkers.icon(
                {"extraClasses": "fa-rotate-0", "icon": "info-sign", "iconColor": "white", "markerColor": "pink", "prefix": "glyphicon"}
            );
            marker_35f247d43f31b67f4ca4c81514576e19.setIcon(icon_481c26120acd2d02759670be6a02a902);
        
    
            marker_35f247d43f31b67f4ca4c81514576e19.bindTooltip(
                `<div>
                     ('340767', 50.97)
                 </div>`,
                {"sticky": true}
            );
        
</script>



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
