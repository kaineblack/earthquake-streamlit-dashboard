# Earthquake Streamlit Dashboard 🗺️
This repository contains a streamlit web application that is connected to the USGS Earthquake API. This API contains near real-time data from earthquake monitoring stations all around the world! 📍

We can then use this dashboard to ...
- Display earthquakes on an interactive Plotly map
- Filter earthquakes by magnitude size
- Filter earthquakes by date of occurence
<br></br>
## What is Streamlit? 📊
Streamlit is a very helpful python library which can be used to help generate beautiful and powerful dashboards that can be deployed as web-applications. They are highly customizable, and the library has an easy to learn syntax which is simple to incorporate into your code. 

[Visit the streamlit website if you want to learn more!](https://streamlit.io/)
<br></br>
## What is the USGS API? 🌎
The USGS (United States Geographic Survery) [provides an open-source API](https://earthquake.usgs.gov/fdsnws/event/1/) which can be queried to access data that is collected from seismographic monitoring stations around the world. We can specify many different parameters when querying the API which makes it easy to get the information we want.
<br></br>
## How to Run the Dashboard 🖥️
Clone this repository on your local machine:
```
git clone https://github.com/kaineblack/earthquake-streamlit-dashboard
```
<br></br>
Install the required dependancies on your python environment: 
```
pip install -r requirements.txt
```
<br></br>
Run the streammlit application (should launch an instance of the application on your browser):
```
streamlit run streamlit_app/eq_dashboard.py
```
<br></br>
<br></br>
## Future Improvements 💡
There is a lot of things we could do with this application in the future to improve its functionality and feature, such as:
- Being able to filter by country/location
- Adding locations for the monitoring stations
- Supplementing the USGS data with additional data from other resources
- Host the application on a cloud server for others to access
- Many more!
