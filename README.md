<h1><center><strong>Africa Data Science Intensive Module 2 Twist</strong></center></h1>

<h1><center><strong>Dennies Bor</strong></center></h1>

<h3><center><a href="https://colab.research.google.com/drive/1xPCV5hS-vMUjU2IkWxQP_Fi3d7ViFa6m#scrollTo=wKQMPCDm7jJY"><strong>COLAB NOTEBOOK</strong></a></center></h3>
<h3><center><a href="www.denniesbor.link"><strong>Deployment</strong></a></center></h3>

<hr />

<h3><center><strong>Project Description</strong></center></h3>
The goal of this twist challenge is to leverage skills gained in module 2, optimization, forecasting and regression in tackling the real world regression problems. In this project, I will investigate Kenya's top five agricultural produce, the pricing, the yields per annum, and regional distribution. I will then use the regression models, specifically random forest regressor to predict the future pricing. This is essential for government planning, and hunger management.
<br/>
<img src="https://github.com/denniesbor/Module2Twist/raw/development/assets/choropleth.png"  />
<br/>
[<strong>Fig 1: Chroropleth of Kenyan counties over which the data is recorded. The color map shows the commodity pricing</strong>]
<br />
Agriculture is one of the main pillars of the Kenyan economy, and the leading revenue generator. The success of any country is dependent on the ability to feed itself. It's unfortunate that cases of hunger deaths are reported annually across the country. According to UN reports, yearly,  2 million Kenyans are starving, equating to 6% of country's population.

<h3><center><strong>Commodity Pricing</strong></center></h3>
The pricing of a commodity in a free market is dictated by the laws of demand and supply. Predicting the future prices of the agricultural commodities will allow the agricultural stakeholders to estimate the supply of these commodities in the market. 
There are many other economic factors which affect the pricing of goods, excluding the supply. These includes money circulation, political atmosphere, government policies, climatic factors, availability and pricing of agricultural inputs, and government expenditure.
<br/>
<img src="https://github.com/denniesbor/Module2Twist/raw/development/assets/price_dist.png"/>

<br />
[<strong>Fig 2: Time variation of commodity pricing.</strong>]
<br />
Kenya compromises of 47 counties, exposed to different climatic and political environments. The populations in these regions vary, and a such will affect the demand of the goods. The product prices are regionally differentiated and there is a likelihood of higher prices in a densely populated region compared to rural regions.

<h3><center><strong>Methods</strong></center></h3>
The first task was to identify the factors which affect the commodity prices. The data used in this task were mined from the government agricultural sites, UN reports, and academic repositories.

<h4><strong>Scope</strong></h4>
The data has been acquired from different web sources. The final dataset is a merger of fertilizer imports, government spending on agriculture, population, political stability indices, quanties of goods produced per region, the population of each region, and climate( averages of temperature and rainfall). These are the features for the use in model training. The commodities of interests are wheat, maize, sorghum, millet, and sweet potatoes as they account for the majority of country's agricultural products.

Due to data unavailable, the duration in which observations were made is limited to 2011 and 2016. So much have changed in terms of climate, but the trends are still relevant. Some of the features have the data aggregated by their annual averages. The monthly gaps are filled with the provided averages.

<h4><strong>Data Collection & Cleaning</strong></h4>
The challenging task in this project is data acquistion, and preparation. Pricing, quantity of produce, fertilizer imports, and government expenditure were acquired from the ministry of agriculture. The climatic and political stability sourced from UN. Cleaning involves formating the data, removing corrupted data, and datatype conversions.

<h4><strong>Database Schema Design</strong></h4>
The cleaned data is stored in a mysql server for querying. Seperate tables are created for each feature. Some features are related, and are linked by foreign or one to one relationship.
<img src="https://github.com/denniesbor/Module2Twist/raw/development/assets/schema.png"  img/>

[<strong>Fig 3: Database scheme. Dotted lines indicates foreign relations</strong>]
<br />

<h4><strong>EDA</strong></h4>
The aim of the EDA is to establish and visualize patterns, trends, relationships and structure of the dataset. The data is queried from the SQL server, and loaded into Pandas dataframe.
<h3><center><strong>Model Training</strong></center></h3>
The final dataframe is a merge of all the tables. The targets are the commodity prices, and the features are trained using the random forest regressor. The model is saved for future inference. The model params are fine tuned with GridSearch CV.

<h3><center><strong>Results</strong></center></h3>
The model performance is evaluated on mean square error. The error is 37, and it's fair considering the amount of training datasets. The model is saved and exported for future inference.
<br />
<img src="https://github.com/denniesbor/Module2Twist/raw/development/assets/maize_preds.png" />
<br />
[<strong>Fig 1: Model performance on maize dataset. The red line indicates the predicted values</strong>]
<br />
<h3><center><strong>Deployment</strong></center></h3>
The model is deployed as a webapp and integrates some of the EDA visualization components. The app is hosted on AWS and it's accessible to the public on <a href="https://www.denniesbor.link">DENNIESBOR.COM</a>

<h3><center><strong>References & Resources</strong></center></h3>
<ol>
<li> Population data: <a href="https://open.africa/dataset/2019-kenya-population-and-housing-census">Open Africa</a></li>
<li> Fertilizer imports: <a href="http://kilimodata.developlocal.org/dataset/kenya-sorghum-production-by-counties">Govt Kilimo Repo</a></li>
<li> Commodity pricing: <a href="http://kilimodata.developlocal.org/dataset/kenya-sorghum-production-by-counties">Govt Kilimo Repo</a></li>
<li> Kenya GeoJSON file:  <a href="https://github.com/mikelmaron/kenya-election-data/tree/master/data">Mikel Maron Github</a></li>
<li> Political Stability data: <a href="https://www.theglobaleconomy.com/Kenya/wb_political_stability/#:~:text=Kenya%3A%20Political%20stability%20index%20(%2D,from%202020%20is%20%2D1%20points.">UN</a></li>
<li> Climate data:<a href="https://africaopendata.org/dataset/kenya-climate-data-1991-2016">Africa Open Data</a></li>
<ol>

