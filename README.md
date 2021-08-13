# Informative Dashboard about Covid Pandemic
Little proyect about an API and a Dashboard focused in the Covid Pandemic. The dashboard show information about the cases, deceases and vaccinations around the world.

![myimagen](/img_readme/covid.png)

## Table of Content
---
- [Goals](#Goals)
- [Installation](#Installation)
- [How to use it](#How-to-use-it)
- [What expected to get](#What-expected-to-get)
- [Requests to the API](#Requests-to-the-API)
  - [Read Database](#Read-Database)
    - [Get](#Get)
    - [Project](#Project)
    - [All together](#All-together)
  - [Insert data](#Insert-data)
  - [Update data](#Update-data)
  - [Delete data](#Delete-data)

## Goals
---
### L1
- [x] Create Api in flask
- [x] Create Dashboard in streamlit
- [x] Database in **MongoDB** or PostgreSWL
### L2
- [x] Use of geospatial data and geoqueries in MongoDB or Postgres (Using PostGIS)
- [x] Have the database in the Cloud (There are free services in MongoDB Atlas, Heroku Postgres, dentre others)
- [x] Generate pdf report of the data visible in Streamlit, downloadable via button.
- [x] A multi-page dashboard in Streamlit.
### L3
- [ ] Have the dashboard send you the pdf report by e-mail
- [ ] To be able to upload new data to the database via API (username and password as request headers)
### L4
- [ ] To be able to update the database via Streamlit (with username and password, in a separate page. The dashboard must make the previous request that adds data via API)
- [ ] Create Docker container and deploy the services in the cloud (Heroku. The two services must be uploaded separately)

## Installation
---
It's necesary to have installed all the libraries of the [requirements.txt](requirements.txt) file. Once you have installed all, you can start running the server and the covid's dashboad

## How to use it
---
To run the dashboard, you just need to put in the console, in the same level where you have the file [streamlit.py](src/streamlit.py), the next commands:
```
streamlit run streamlit.py
```

If all worked OK, in the console you must have an IP direcction. Copy and paste the IP in your internet explorer and you shoud have acces to the dashboard.
![myimage](img_readme/dashboard.PNG)

## What expected to get
---
This dashboard is focused in show in a simple format data about the Covid19 Pandemic. The cases of covid, deaths and recovered people in every country around the world up to date. Also, it show a graphic about the evolution of covid for every country you selected.
![myimage](img_readme/graph.PNG)

You can choose a range of days to show the covid evolution. For example, you can choose to se the evolution evey seven days, or every 20 days, or even every 3 months. You just need to adjust the values and wait for the graph the show the data.

![myimage](img_readme/range.PNG)
![myimage](img_readme/graph_3_months.PNG)

It also show a map of the world with a mark in every country you selected to see the data.

![myimage](img_readme/map_world.PNG)

To end the first page of the dasboard, there is a button the let you download the data from the graph and the graph it self. The data of the graph is in JSON format, so you can use it in other project just by copy and paste it.
___
The second page of the dashboard will focused on the cases in Autonomous Communities in Spain. In this case, the data will be showed as a table and the data will depend the type of data that you want to show. In this case, "Deaths" or "Vaccination".

![myimage](img_readme/CCAA.PNG)
![myimage](img_readme/CCAA_data.PNG)

The Download button work on the same way as the button in the first page, storaging a pdf with the showed data in JSON format.

## Requests to the API
---
At the moment, tha API can receive get,update and delete requests. All the countries are included in the databse, so you can select the one you want, more than one or all of them. The endpoint to make the requests is:
```
http://127.0.0.1:3500/get
http://127.0.0.1:3500/post
http://127.0.0.1:3500/update
http://127.0.0.1:3500/delete
```
To acces to the data of the deceases, recovered, or the data of the Autonomous Communities of Spain, you must specified it just after the get endpoint.

The data you can acces and the endpoint is listed in the next table.

|Database|Endpoint|
|--------|--------|
|Cases of covid|*It no need any endpoint|
|Deceases|deaths|
|Recovered|recovered|
|Covid data of the Autonomous Communities|ccaa_data|
|Vaccination data of the Autonomous Communities|ccaa_vac|

## Read Database
### Get
- To get the data of the vaccination in the Autonomous Communities of Spain, the request must be done to:
```
http://127.0.0.1:3500/get/ccaa_vac
```

- If what we want is to get all the data from the database selected, the Query Params must be "All"
```
http://127.0.0.1:3500/get/ccaa_vac?All
```
- If we want the cases data from a specific country, the Query Params must be "Country/Region":
```
http://127.0.0.1:3500/get?Country/Region=Germany
```
*To get the information of more than one countries, just name them separated by commas without spaces between them.

- If what you want it's to get the countries that have more/less than X's cases of covid, deceases or recovered, the Query Parameter must be "Cuantity", followed by the correct mathematical symbol (<,>,>=,<=) and the number separated by commas.
```
http://127.0.0.1:3500/get?Cuantity=>,100_000

                    or    

http://127.0.0.1:3500/get?Cuantity=>,100000 
```
- To set a range, it must have the same order. That to say: "The countries that have more than or equal of 150_000 recovered and less than 300_000"
```
http://127.0.0.1:3500/get/recovered?Cuantity=>=,150_000,<,300_000
```

### Project
- All of these request, return the name of the country with the data of the every days since the goberments start publicating the data but, if we only want to know the country or the total of people affected, we can do it by adding anotherQuery Parameter.
```
http://127.0.0.1:3500/get?project
```
- This alone wont work, you must specified the data you want to show. In this case, we can use "Country/Region" to get the name of the country or/and "Total", to get the total of people that have been affected, deceased or recovered by the covid pandemic. Remember that if you want to get both, you must separated them by commas without spaces.
```
http://127.0.0.1:3500/get?project=Country/Region,Total
```

### All together
-To end this section, we gonna show you a complete request using both parts, the get and the project. This will be the format than will need to have al the request. You can ommitted the project part but remember that the reponse you will obtain will be the cases, deceased or whatever for every day since the begining of the covid pandemic.
- Simple requests
  - The total cases of covid in Spain, Germany and Canada, showing the total number and the name of the country:
  ```
  http://127.0.0.1:3500/get?Country/Region=Spain,Germany,Canada&project=Country/Region,Total
  ```
- More complex request
  - From a list of countries (**Spain, Andorra, Canada, Afghanistan, Bangladesh, Botswana, Chile, Colombia, Indonesia, India, Iran**), I want to get all of them that the number of deceased are between 50_00 and 100_000 and show me the name of the country and the total of deceased.
  ```
  http://127.0.0.1:3500/get/deaths?Country/Region=Spain,Andorra,Canada,Afghanistan,Bangladesh,Botswana,Chile,Colombia,Indonesia,India,Iran&Cuantity=>=,50_000,<=,100_000&project=Country/Region,Total
  ```

## Insert data
To insert new data to the databse, you must pass to the request the new data in the same format you did the lasts requests. Every Query Parameter is a new column, and the value of the Query Parameter the value of the column.
- Want to add the EEUU to the databse and only with one column, the total cases of covid up to date.
    ```
    http://127.0.0.1:3500/post?query=Country/Region=EEUU&8/13/21=36_868_469
    ```

## Update data
To update data in the database, you must create a request that return the country that you want to modify and then set the field that you want to change. For example:
- Want to change the total of cases in Spain at date 8/3/21. The real number of decease were 81_793
    ```
    http://127.0.0.1:3500/update?query=Country/Region=Spain&new_data=8/3/21=81_793
    ```

## Delete data
To delete data, you also must put a wuery that returns you at least one country.
- Lets delete Spain from the database so nobody see the disaster happened here ...
    ```
    http://127.0.0.1:3500/delete?Country/Region=Spain
    ```