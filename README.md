<h2 align = "center">NYC Traffic Open Data: Notice of Project Objectives and Limitations</h2>
<hr>

<i>This is a semester-long project for the course <b>ARTS-UG 1647 Making Virtual Sense</b> at <b>New York University, Gallatin School of Individualized Study</b></i>.

<i>--- Developed under the advice of <b>Doctor Carl Skelton</b>, solely by <b>Michael Xu</b> (NYU NetID: tx542; Full Legal Name: Tianxiao Xu)</i>

<i>A <b>demonstration ("demo") of the end product</b> described in this document (sample size = 1000 data points) is published on the World Wide Web (WWW) <b>at the URL <a href = "https://traffic-demo.herokuapp.com/" target="_blank">https://traffic-demo.herokuapp.com/</a></b>. Usage of this end product demo is contingent upon the terms and conditions listed in this "Notice of Project Objectives and Limitations" document.</i>

<hr>

<h3 align = "center">OUTLINE</h3>
<h4>1. Project Disclaimer and Purpose</h4>
<h5>1.1 Project Disclaimer ("Disclaimer")</h5>
<h5>1.2 Project Purpose & Objectives ("Manifesto")</h5>
<h5>1.3 Project Simulator Specifications ("Instructions")</h5>
<h4>2. Project Data Sources and References</h4>
<h5>2.1 Citation of Critical Data Sources, Programming Libraries/Packages, and Services</h5>
<h5>2.2 Citation of All Used Python Programming Libraries</h5>
<h4>3. Project Methodology, Limitations, and Directions for Future Research</h4>
<h5>3.1 Limited Sample Size</h5>
<h5>3.2 Variables Used, KNN Models, and Losses in the Degrees of Freedom</h5>

3.2.1 Descriptive Illustrations of Traffic Data<br>
3.2.2 Aesthetic Considerations (Map Color Scheme)<br>
3.2.3 Predictive Models (KNN Approach)<br>
3.2.4 Losses in the Degrees of Freedom

<h5>3.3 Ethical Considerations in User Proposals</h5>
<h5>3.4 Directions for Future Research</h5>
<h4>4. Contact Information</h4>

<hr>

### 1. Project Disclaimer and Purpose

#### 1.1 Project Disclaimer ("Disclaimer")
**IMPORTANT:**

**Though this project indeed (factually) produces a functioning prototype of a descriptive and predictive simulator of NYC traffic network patterns that permits interactive user specifications, its main objectives are artistic and illustrative, rather than functional and utilitarian. The project developer thus requests that all end-users use the simulator (as an artistic and illustrative end product of this project) accordingly.**

**It shall NOT be used as a model from which extrapolating inferences or generalizations can be made to the real world.**

**Furthermore, for any user-inputted proposal regarding the construction of a new "Road" or "Multi-Road" (see definition in section 1.3 below), this artistic and illustrative simulator will generate a list of warnings ("ethical considerations") regarding the areas and people negatively impacted by this proposal (based on the listed stopping points).**

**Indeed, this feature illustrates the necessity of the incorporation of ethical considerations in actual models adapted for real-life urban planning in the real world (NOT within the scope of this artistic and illustrative simulator). Such incorporation of ethical considerations would help the end-users more accurately discern the potential socioeconomic costs of their proposal, which may further inform and facilitate their marginal analysis and decision-making processes.**

#### 1.2 Project Purpose & Objectives ("Manifesto")

This project has largely drawn inspiration from Doctor Carl Skelton's work <i><a href = "https://uttri.utoronto.ca/files/2019/05/CitizenInformaticsCleaned01reduced.pdf" target="_blank">Citizen Informatics: Integrating Urban Data and Design for Future Stakeholders</a></i>. The project is developed with the aim that big data—especially real-time data points pertaining to descriptive features related to urban planning—should not only be made **publicly available**, but also **easily accessible, manipulable, and operable** by any citizens as **direct and active participants to urban planning in the *planning* stage** (e.g. as proposers of policies/models, independent evaluators of existing proposals, operators of big data for statistical inferences, etc.). 

It further concurs with the nascent notion that *literacy* shall be redefined to include *data literacy* in our era of big data and digitalization, and that *standards of literacy* are not only those *crude and passive*, but rather must also include the ability, of the literate population, to **make sense of, manipulate, and thereby create new content using existing information**. 

This project focuses on **modeling the traffic network patterns of the City of New York**, due to considerations that traffic networks largely define modern physical mobility, a characteristic essential to models in the social sciences ranging from economic analyses to urban planning (optimizing citizen life quality/living experience). Furthermore, citizens/residents of the City of New York are already automatically (and oftentimes unwittingly) *passive participants in the city's traffic network*. It is meaningful and rightfully pertaining to civil duties that they may be empowered with the *easily accessible, manipulable, and operable* big data information so that they may become *active and literate participants* in the planning of the traffic network of the City.

With regards to the **public availability of open data**, the City of New York shall be recognized and commended for its easily accessible <i><a href = "https://opendata.cityofnewyork.us/" target = "_blank">public open data database</a></i>. Nonetheless, for instance, its <i><a href = "https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/qkm5-nuaq" target = "_blank">Real-Time Traffic Speed Data</a></i> provided by the NYCDOT (<i><a href = "http://nyctmc.org/ " target = "_blank">New York City Department of Transportation</a></i>) is **NOT easily accessible, manipulable, and operable at all**. A simple glance over the dataset can reveal that it is poorly organized (left in a tabular form, without even any descriptive statistics), presented in string (and thus non-machine-readable nor -analyzable) formats, and without informative and visual illustrations. 

Therefore, with the broader objective of **supporting, informing, and encouraging broad public participation in urban (traffic) planning**, the developer of this project has developed a functioning prototype of a **descriptive and predictive simulator of NYC traffic network patterns that permits interactive user specifications (the exact functions to be specified in section 1.3 below)**. Of course, due to the limited scope of this project, the end-product is more of an **artistic and illustrative prototype**, and **shall NOT be used as a model from which extrapolating inferences or generalizations can be made to the real world**.

It will, nonetheless, call on and invite scholars and experts in the relevant fields, to pay attention and efforts to **figuratively construct the bridge that is necessary to connect public datasets (in non-user-friendly formats) with end-users (who may not necessarily have great skills or expertise in data science, statistical inferences and modeling, or relevant fields), thereby fostering broad public participation in urban (traffic) planning—with minimum assumptions/skill requirements, but rather maximum inclusion of the end-users as modern citizens in urban settings**.

#### 1.3 Project Simulator Specifications ("Instructions")
*Note: this instruction is appended to the header of the actual simulator itself as well, for easier access and to avoid confusion in operations.*

<b>Instructions:</b>

You have <b>four</b> possible modification options (different scenarios) to run the simulation with:
<ol>
  <li><b>None: No modifications.</b> You can <b>select a borough</b> in the <i>Borough</i> section to view a descriptive 
  interactive illustration (on the map below) of the traffic network patterns of the <i>entire borough</i>. Note: 
  viewing the traffic information and metadata of a specific street has been depreciated, due to the interdependent and 
  inter-correlated nature of traffic networks on the borough level. </li>
  
  <li><b>Construction: Place a specific road under construction.</b> You can select a borough in the <i>Borough</i> section, 
  and the name of a specific street (with real-time surveillance data available from the 
  <i><u><a href = "https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/qkm5-nuaq" target="_blank" style="color:blue;">
  NYC Open Data database</a></u></i>) of that borough in the <i>Traffic Link ...</i> section to place it under construction. 
  And as this road will be under construction, it will be taken down from the overall
  traffic network, thereby (likely) influencing the borough-level traffic patterns. </li>
  
  <li><b>New Road: Proposal to build a new road (in addition to the existing "grid" traffic network).</b> 
  You will <b>only</b> need to enter the street address (as accurate as possible) of the <b>starting point</b> in the 
  <i>Starting Point</i> section, and that of the <b>ending point</b> in the <i>Ending Point</i> section. 
  You won't need to enter anything else in any other sections (they will be invisible anyway, to avoid confusion).</li>
  
  <li><b>New Multi-Road: Proposal to build a new road, with multiple stopping points.</b> In the <i>Multi-Road</i>
  text box, enter the street address of each of the proposed stopping points in a new line (separate by the <i>enter/return</i> key). 
  Make sure that the address for every location is <b>accurate (to the best of your knowledge)</b>—otherwise,
  the simulator may not be able to locate your proposed point and return an error. </li>
</ol>

### 2. Project Data Sources and References

#### 2.1 Citation of Critical Data Sources, Programming Libraries/Packages, and Services
- <b>Source of Raw Data:</b> 
    - <i><a href = "https://opendata.cityofnewyork.us/" target = "_blank">NYC Open Data dataset</a></i>, published by the City of New York
    - <i><a href = "https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/qkm5-nuaq" target = "_blank">Real-Time Traffic Speed Data</a></i> provided by the NYCDOT (<i><a href = "http://nyctmc.org/ " target = "_blank">New York City Department of Transportation</a></i>)
    
    
- <b>Folium Python Library (for visualization of metadata on an interactive map):</b> 
    - <a href = "https://leafletjs.com/">Leaflet</a> | Data by © <a href = "http://openstreetmap.org/">OpenStreetMap</a>, under <a href = "http://www.openstreetmap.org/copyright">ODbL</a>.
    
    
- <b>Search Queries API (to look up location metadata based on user-inputted address):</b>
    - OpenStreetMap (OSM) - Nominatim © OpenStreetMap contributors. 
    - OpenStreetMap® is open data, licensed under the Open Data Commons Open Database License (ODbL) by the OpenStreetMap Foundation (OSMF). The data is available under the Open Database License. https://www.openstreetmap.org/copyright


- <b>Population Estimation Service (for ethical considerations: estimating the negatively impacted population):</b>
    - Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Population Estimation Service, Version 3 (PES-v3). Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4DR2SK5. Accessed December 2021. https://sedac.ciesin.columbia.edu/data/collection/gpw-v4/population-estimation-service

#### 2.2 Citation of All Used Python Programming Libraries 
<i> Produced using <a href = "https://pypi.org/project/citepy/">citepy</a></i>

Ahmed TAHRI @Ousret. (2021, December 3). charset-normalizer. GitHub. https://github.com/ousret/charset_normalizer (Original work published 2019)

Alex Grönholm. (2021, November 22). anyio. The Python Package Index. https://pypi.org/project/anyio/ (Original work published 2018)

Chris L. Barnes. (2021, May 11). citepy. GitHub. https://www.github.com/clbarnes/citepy (Original work published 2019)

Daniel Holth. (2021, August 9). wheel. GitHub. https://github.com/pypa/wheel (Original work published 2012)

Hynek Schlawack. (2021, May 7). attrs. attrs.org. https://www.attrs.org/ (Original work published 2015)

Ian Stapleton Cordasco. (2021, May 7). rfc3986. ReadTheDocs. http://rfc3986.readthedocs.io (Original work published 2014)

Isaac Muse. (2021, November 11). soupsieve. GitHub. https://github.com/facelessuser/soupsieve (Original work published 2018)

Julian Berman. (2021, November 5). jsonschema. GitHub. https://github.com/Julian/jsonschema (Original work published 2012)

Kenneth Reitz. (2021, October 8). certifi. ReadTheDocs. https://certifiio.readthedocs.io/en/latest/ (Original work published 2011)

Kim Davies. (2021, October 12). idna. GitHub. https://github.com/kjd/idna (Original work published 2013)

Leonard Richardson. (2021, September 8). beautifulsoup4. crummy.com. http://www.crummy.com/software/BeautifulSoup/bs4/ (Original work published 2013)

Nathaniel J. Smith. (2020, October 11). sniffio. GitHub. https://github.com/python-trio/sniffio (Original work published 2018)

Nathaniel J. Smith. (2021, January 1). h11. GitHub. https://github.com/python-hyper/h11 (Original work published 2016)

Python Packaging Authority. (2021, December 5). setuptools. GitHub. https://github.com/pypa/setuptools (Original work published 2006)

The pip developers. (2021, October 22). pip. pip.pypa.io. https://pip.pypa.io/ (Original work published 2008)

Tobias Gustafsson. (2021, June 28). pyrsistent. GitHub. http://github.com/tobgu/pyrsistent/ (Original work published 2013)

Tom Christie. (2021a, November 16). httpx. GitHub. https://github.com/encode/httpx (Original work published 2019)

Tom Christie. (2021b, November 17). httpcore. GitHub. https://github.com/encode/httpcore (Original work published 2019)


### 3. Project Methodology, Limitations, and Directions for Future Research

#### 3.1 Limited Sample Size
In the published **demonstration ("demo") of the end product**, a **most recent sample of 1,000 data points is requested from the server of the <i><a href = "https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/qkm5-nuaq" target = "_blank">Real-Time Traffic Speed Data</a></i> dataset**. This is largely due to considerations of the **compatibility** (in computing powers) of different devices and operating systems—**1,000 data points would still be statistically large enough** (for theorems such as the *Law of Large Numbers* or *Central Limit Theorem* to hold—which are essential for key model assumptions such as an identifiable asymptotically normal distribution for model estimators/statistics), while **not so large that the server queries place significant burdens on the devices of end-users** (or the queries may simply take too much time and negatively impact user experiences). 

Nonetheless, the size of the entire population of the aforementioned dataset is 56,402,763 (as of 17:08 EST, Wednesday, Dec. 8, 2021), and this number is constantly increasing with more recent traffic surveillance observations being uploaded to the server. Thus, the sample being studied in this simulator (and its relevant models) **may not necessarily be representative of the behavioral variations of traffic network patterns within boroughs across time in its entirety**—due to practical considerations and the limited scope of this project—thus **statistical inferences with real-world implications should NOT be drawn from this simulator, as consistently mentioned above**. 

#### 3.2 Variables Used, Predictive (KNN) Models, and Losses in the Degrees of Freedom

##### 3.2.1 Descriptive Illustrations of Traffic Data
For the first step, from the source <i><a href = "https://data.cityofnewyork.us/Transportation/Real-Time-Traffic-Speed-Data/qkm5-nuaq" target = "_blank">Real-Time Traffic Speed Data</a></i> dataset, only the variables `SPEED` (renamed as `rou_speed` in the model dataframe), `TRAVEL_TIME` (renamed as `tr_time` in the model dataframe), `DATA_AS_OF` (renamed as `time_s` in the model dataframe), `LINK_POINTS` (transformed from `string` into a Python `LineString` object, under the new column variable label `geometry`), `BOROUGH` (renamed as `boro` in the model dataframe), and `LINK_NAME` (renamed as `names` in the model dataframe) are requested and stored locally in the model (each having been processed as respectively indicated in the parentheses next to the variable label). These pieces of information have been sufficient for the purpose of **descriptive illustrations of traffic network patterns (travel time, travel speed, and metadata) on the borough level**.

##### 3.2.2 Aesthetic Considerations (Map Color Scheme)
For artistic illustration purposes (which is the nature of this simulator and its demonstration), the background of the map on which each road is denoted has been intentionally chosen as **"black and white" (following the `Stamen Toner` style of the `Folium` Python library)**—simultaneously reminiscent of comic strips and placing more emphasis on the roads (visible as a **colored geometric trajectory by plotting the respective `LineString` object for each road**), as well as the HTML markers placed at the starting point of each road (where the users can click on them to learn about more metadata-information related to the road).

The color scheme for the road trajectories are as follows:
- <b style="color:#BB1E10;">Red (hex code: #BB1E10):</b> if the speed at the chosen point in time is **slower than or equal to** the historical average of this road
- <b style="color:#33A532;">Green (hex code: #33A532):</b> if the speed at the chosen point in time is **faster** than the historical average of this road
- <b style="color:#F7B500;">Yellow (hex code: #F7B500):</b> if changes are proposed to the road (see sections below for more details)

This color scheme has been intentionally chosen as it follows the **color scheme of the vehicle traffic light signals of the State of New York**. 

##### 3.2.3 Predictive Models (KNN Approach)

Apart from the purely descriptive illustrations, all the other functions ("Construction", "New Road", "New Multi-Road") of this simulator necessarily involve predictive modeling. The model approach of **KNN (K-Nearest Neighbors)**, provided by the `scikit-learn` Python library, has been chosen by the developer—with the **following important considerations**:
- The KNN model uses Euclidean distance to identify the "nearest neighbors" (from the existing data of roads that have been used to fit the model) that would behave **most similarly to the completely new and never-seen-before road (in the case of proposing a new road) and network system (in the case of placing a road under construction)**. This similarity in behaviors and properties of roads belonging to a traffic network system clustered on the level of boroughs is thus highly intuitive and essential to the developer's adaptation of KNN models in predictions. 


- Based on the developer's own past experiences and experimentations, **the KNN approach behaves more consistently and reliably than other common alternative machine learning models** such as random forests (RF) or logistic regressions. Some important reasons would be that random forests (RF) models, which involve binary decision trees, tend to yield similar if not the same outputs for a range of inputs (or input bundles). And as for logistic regressions, the developer has learned from another machine learning class that programmers cannot identify the optimal hyperparameter using conventional train-test split or cross-validation methods. 
    - Read further about a comparison of different prediction models and approaches <a href = "https://github.com/tx542/db_mid/blob/main/bsg9679_sgt2559_tx542_Assignment_3_vFinal.ipynb" target = "_blank">here (a group project in another class, of which the developer has been a part)</a>.
    
    
- The full model of the simulator would find the optimal hyperparameter of the KNN model (the number of "nearest neighbors") through a combination of train-test split and cross-validation every time a new set of samples is queried from the dataset server. Nonetheless, this would be extremely **computationally costly and not conducive to interactive user experiences**. Thus, **for the demonstration of the simulator, the optimal hyperparameter (based on historical average) of `7 nearest neighbors` is used for the KNN models**.

##### 3.2.4 Losses in the Degrees of Freedom
Statistically speaking, up to **three degrees of freedom can be lost** in the predictive models—as the **KNN models are used more than once using the same sample from the dataset to gauge population relationships of interest** (depending on the specific user's choice of predictive functions):

- In the case of the **"Construction" predictive function, two degrees of freedom** are lost, as:
    - `names_code` (name of the roads in the traffic network, turned into encoded strings to fit into KNN models), `boro_code` (borough of the road turned into encoded strings for the same reason), `time_float` (`time_s` turned into `pandas.timestamp` object to fit into KNN models), and `tr_dist` (the `length` attribute of the Python `LineString` object for each road) are used to estimate (predict) the `tr_time` (travel time) of each road in the new, modified traffic network (having placed a road under construction);
    - Then, `names_code`, `boro_code`, `time_float`, `tr_dist`, and the estimated (predicted) `tr_time` are used to again estimate (predict) `rou_speed` (travel speed) of each road in the new, modified traffic network, using the same sample dataset. 

    In other words, if we regard the KNN models as functions (as there can be only one output for each bundle of input), and define the first step (KNN model) as $\text{KNN}_1: \mathbb{R}^4 \to \mathbb{R}$ and the second step  (KNN model) as $\text{KNN}_2: \mathbb{R}^5 \to \mathbb{R}$, we have:
    
        - $\hat{\text{tr_time}} = \text{KNN}_1(\text{names_code}, \text{boro_code}, \text{time_float}, \text{tr_dist})$
        - $\hat{\text{rou_speed}} = \text{KNN}_2(\text{names_code}, \text{boro_code}, \text{time_float}, \text{tr_dist}, \hat{\text{tr_time}})$
        
     **Using the same dataset, we have two levels of estimates—hence the loss of two degrees of freedom**.


- In the case of the **"New Road" and "New Multi-Road" predictive functions, three degrees of freedom** are lost, as:
    - First of all, we need to determine **to which existing roads ("nearest neighbors") this newly proposed road behaves most similarly** (which happens to be the underlying intuition behind the KNN approach): we use `boro_code`, `time_float`, and `tr_dist` to estimate (predict) `names_code`.
    - Then, we follow the same steps as above: 
        - Use the estimated (predicted) `names_code`, `boro_code`, `time_float`, and `tr_dist` to estimate (predict) the `tr_time` (travel time) of each road in the new traffic network (with the addition of a newly proposed road).
        - Use the estimated (predicted) `names_code`, `boro_code`, `time_float`, `tr_dist`, and the estimated (predicted) `tr_time` to again estimate (predict) `rou_speed` (travel speed) of each road in the new traffic network, using the same sample dataset. 
        
    In other words, if use the same KNN function definitions as scenario 1 above, and also define the "first of all - gauging the `names_code` of the road" step as $\text{KNN}_0: \mathbb{R}^3 \to \mathbb{R}$, we have:
    
        - $\hat{\text{names_code}} = \text{KNN}_0(\text{boro_code}, \text{time_float}, \text{tr_dist})$
        - $\hat{\text{tr_time}} = \text{KNN}_1(\hat{\text{names_code}}, \text{boro_code}, \text{time_float}, \text{tr_dist})$
        - $\hat{\text{rou_speed}} = \text{KNN}_2(\hat{\text{names_code}}, \text{boro_code}, \text{time_float}, \text{tr_dist}, \hat{\text{tr_time}})$ 

    <b>Using the same dataset, we have three levels of estimates—hence the loss of three degrees of freedom</b>.
    
Please refer to this document (Jupyter Notebook) for a more comprehensive analysis of the predictive machine learning models that the developer has experimented with for this project (LINK TO BE ADDED SOON).

#### 3.3 Ethical Considerations in User Proposals

In considerations of ethical implications associated with urban (traffic) planning proposals, for **any user-inputted proposal regarding the construction of a new "Road" or "Multi-Road"** (see definition/instruction in section 1.3 above), the simulator will generate a **list of warnings ("ethical considerations") regarding the areas and people negatively impacted by this proposal (based on the listed stopping points)**.

Indeed, this feature illustrates the **necessity of the incorporation of ethical considerations in actual models adapted for real-life urban planning** in the real world (NOT within the scope of this artistic and illustrative simulator). Such incorporation of ethical considerations would help the end-users **more accurately discern the potential socioeconomic costs of their proposal, which may further inform and facilitate their marginal analysis and decision-making processes**.

The information and data pertaining to these ethical considerations have been obtained through the **OpenStreetMap (OSM) - Nominatim © API and the Population Estimation Service (PES) web-based service** (cited in section 2.1 above). 

The OpenStreetMap (OSM) - Nominatim © API provides **metadata regarding a certain OSM address object that can be identified through search queries based on user-inputted addresses (string format)**. The following pieces of information have been incorporated into the ethical analyses of this project (simulator and demonstration):
1. Full address name
2. Latitude and longitude
3. OSM class
4. OSM type
5. OSM importance index
<br><a href = "https://nominatim.org/release-docs/develop/api/Output/#json" target = "_blank">Learn more about Nominatim © API place search output formats and information here</a>

With regards to the **Population Estimation Service (PES) web-based service**, the minimum area (for which an estimate can be obtained through the service) is the equivalent of **a circle with a radius of 5km ($25\pi \approx 78.5398\text{ km}^2$)**. If the user proposes a new road construction plan that involves **an area less than the aforementioned minimum, an estimate is obtained through secondary calculations by scaling down the minimum area using the ratio of areas (i.e. user proposal area to PED minimum area)**.

The following datasets have been used for ethical analyses of this project (follow <a href = "https://docs.google.com/spreadsheets/d/1W9Zg2kHF0xEJ-1cS_IZLOgFIHAFf-CFG079ScrE05RA/edit#gid=0" target = "_blank">this link</a> for a list of the available datasets provided by the PES):
1. Population Count, v4.10 (2000, 2005, 2010, 2015, 2020) - `gpw-v4-population-count-rev10_2020`
2. UN WPP-Adjusted Population Count, v4.10 (2000, 2005, 2010, 2015, 2020) - `gpw-v4-land-water-area-rev10_landareakm`

#### 3.4 Directions for Future Research

As demonstrated in the linked Jupyter Notebook document (you may also follow this link - TO BE ADDED) in section 3.2.4 above, even the optimal models for some of the intermediary steps in estimating (predicting) traits of roads in a newly defined traffic network under user specifications may not necessarily be **very strongly explanatory of the variations in the sample dataset with high cross-validation of train-test split scores (which are some variations of $R^2$ that evaluates the goodness-of-fit of statistical models)**. Indeed, this suggests the existence of **additional omitted or confounding (lurking) variables not included in the models** throughout this project. 

Therefore, one promising direction for future research and projects in similar fields would be the adaptation of **agent-based microsimulation models**, which can account for the **demand side of traffic usage (arising from the NYC citizen/resident population)**, which would certainly be associated with network patterns on the borough level. The adaptation of agent-based microsimulation models has not been possible for the scope of this project—due to the lack of appropriate datasets, the limits of the developer's relevant skill sets, and the absence of relevant, ready-to-use libraries implemented in the Python programming language. 

Additionally, one could also explore the **heterogeneity in the exact mode of transportation—ranging from pedestrians (walking) or biking to taking public transit (with buses or MTA)**. A study of this more comprehensive spectrum of circulations (mobility) could shed further light on the factors contributing to individuals' choices of a (more preferred) mode of transportation, as well as the likely different types of population-level relationships and predictive models across different means of circulations (physical mobility). 

### 4. Contact Information

This project is a semester-long project for the course ARTS-UG 1647 Making Virtual Sense at New York University, Gallatin School of Individualized Study. It has been developed under the advice of Doctor Carl Skelton, solely by Michael Xu (NYU NetID: tx542; Full Legal Name: Tianxiao Xu). 

For any pertinent inquiries (from comments/feedback on this project to further academic discussions), please reach out to the sole project developer, <b>Michael Xu, at <a href = "mailto:michael.xu@nyu.edu">michael.xu@nyu.edu</a></b>. Note that the sole project developer is an undergraduate student at New York University Abu Dhabi. 

<hr>
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
