import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import plotly.express as px

API_KEY = "71872bc24cff61937c28cc1555974ae1"


def get_data(place, forecast_days=None):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]
    nr_values = 8 * forecast_days
    filtered_data = filtered_data[:nr_values]
    return filtered_data

def get_wind_speed(dict):
    return dict["wind"]["speed"]

st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecast days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky", "Wind"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Dates", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115, caption=dates)
        if option == "Wind Speed":
            images = {"Wind": "images/wind.png"}
            wind_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            wind_speeds = [get_wind_speed(dict) for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            
            # Check if wind speed exceeds 2 km/h
            wind_anomaly_indices = [i for i, speed in enumerate(wind_speeds) if speed > 20]

            # Create a list of indices for wind anomalies
            wind_anomaly_paths = [index for index, speed in enumerate(wind_speeds) if index in wind_anomaly_indices]
            image_paths = [images[condition] for condition in wind_conditions]
            
            st.write("Wind anomaly (speed above 2 km/h):")
            st.image([image_paths[i] for i in wind_anomaly_paths], width=115, caption=[dates[i] for i in wind_anomaly_paths])


           

    except KeyError:
        st.write("That place does not exist.")