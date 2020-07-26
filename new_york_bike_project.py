import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import pydeck as pdk
st.title("First Streamlit Web Application")
st.markdown("markdown")

@st.cache(persist=True)
def load_data(nrows):
    df= pd.read_csv("/Users/ahmetemintek/Desktop/streamlit/medium_blog/NYC-BikeShare.csv",
                    nrows= nrows)
    df.dropna(inplace=True)
    lowercase= lambda x: str(x).lower()
    df.rename(lowercase, axis="columns", inplace=True)
    df.rename(columns={"start station latitude": "latitude",
               "start station longitude": "longitude",
               "user type": "user_type",
                "start station name": "start_station_name",
                "birth year": "birth_year"}, inplace=True)
    return df
data_fr= load_data(100000)
df= data_fr.copy()

if st.checkbox("Show/Hide Data", False):
    st.subheader("Rows")
    st.write(df)

df["start_time"]= pd.to_datetime(df["start time"])
st.header("How many bikes are rented at a given time of day?")
hour= st.selectbox("Hour to look at", range(0,24), 1)
data= df[df["start_time"].dt.hour==hour]
st.write(data)

st.header("Bike Rentals By Day Of The Month")
df["start_day"]= df["start_time"].dt.day
days= st.slider("Day To Look At", 1,31)
st.map(df.query("start_day== @days")[["latitude", "longitude"]])

st.header("Bike Rentals By Day Of Month")
hist= np.histogram(df["start_time"].dt.day, bins=31, range=(0,31))[0]
chart_data= pd.DataFrame({"Day": range(0,31), "Rentals": hist})
fig= px.bar(chart_data, x="Day", y="Rentals", hover_data=["Day", "Rentals"], height=300)
st.write(fig)

st.header("3D Map")
midpoint=[np.average(df["latitude"]), np.average(df["longitude"])]
st.pydeck_chart(pdk.Deck(
            map_style= "mapbox://styles/mpbox/light -v9",
            initial_view_state= {
                "latitude": midpoint[0],
                "longitude": midpoint[1],
                "zoom": 11,
                "pitch": 50,
            },
            layers=[
                    pdk.Layer(
                        "HexagonLayer",
                        data= df[["start_time","latitude","longitude"]],
                        get_position= ["latitude","longitude"],
                        radius=200,
                        elevation_scale=4,
                        elevation_range=[0,1000],
                        pickable= True,
                        extruded= True,
                    ),
            ]

)
)
