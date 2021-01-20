import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express  as px

st.title("Analyse Accidents ")
st.markdown("## Motor Vehcile Collision on New york city")

DATA_URL= ("Motor_Vehicle_Collisions_-_Crashes.csv")
DATE_TIME = "date/time"
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"crash_date_crash_time": "date/time"}, inplace=True)
    #data = data[['date/time', 'latitude', 'longitude']]
    return data 

## displaying the raw data
data=load_data(10000)



## displaying the map
st.header("Where are the most people injured in NYC")

#adding slider to sidebar
injured_people=st.sidebar.slider("Number of persons injured in people collision",0,19)
st.map(data.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any"))


st.header("how many collisions occur during given time of day")
hour= st.selectbox("Hour to look at ", range(0,24),1)
original_data = data
data =data[data['date/time'].dt.hour==hour]

if st.checkbox("Show raw Data",False):

    
    st.subheader("Raw Data")
    st.write(data)

st.markdown("Vehicle collision between %i:00 and %i:00" % (hour,(hour+1)  %24))

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))


st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
        layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['date/time', 'latitude', 'longitude']],
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        radius=300,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0, 1000],
        ),
    ],

))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data[DATE_TIME].dt.hour >= hour) & (data[DATE_TIME].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})

fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header("Top 5 dangerous streets by affected class")
select = st.selectbox('Affected class', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how="any")[:5])

elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how="any")[:5])

else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how="any")[:5])
















