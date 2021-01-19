import streamlit as st
import pandas as pd
import numpy as np

st.title("Analyse Accidents ")
st.markdown("## Motor Vehcile Collision on New york city")

DATA_URL= ("Motor_Vehicle_Collisions_-_Crashes.csv")

@st.cache(persist=True)
def load_data(nrows):
    data=pd.read_csv(DATA_URL,nrows=nrows, parse_dates=[["CRASH_DATE","CRASH_TIME"]])
    data.dropna(subset=["LATITUDE","LONGITUDE"], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplac=True )
    data.rename(columns={"crash_date_crash_time": "date/time"},inplace=True)
    return data

data=load_data(10000)










