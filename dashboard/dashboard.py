import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Judul
st.title(":bar_chart: Bike-Sharing Dashboard")

# Load Dataset
bike_dataset = pd.read_csv("https://raw.githubusercontent.com/faqhmlna0/Proyek-Akhir-Python-for-Data-Analyst/main/bike_dataset_data.csv")
bike_dataset['date_day'] = pd.to_datetime(bike_dataset['date_day'])

# Weather
def create_weather_total(bike_dataset):
    weather_total = bike_dataset.groupby("weather_daily").agg({"total_count_hourly": lambda x: x.sum()})
    weather_total = weather_total.reset_index()
    weather_total = weather_total.rename(columns={"total_count_hourly": "total_riders"})
    weather_total['season_daily'] = pd.Categorical(weather_total['weather_daily'],
                                                   categories=['Clear','Mist','Light Snow', 'Heavy Rain'])
    weather_total = weather_total.sort_values('weather_daily')
    return weather_total

# Menghitung Total Pengguna per Cuaca
weather_total = create_weather_total(bike_dataset.dropna())

# Season
def create_seasonly_total(bike_dataset):
    seasonly_total = bike_dataset.groupby("season_daily").agg({"total_count_hourly": lambda x: x.sum()})
    seasonly_total = seasonly_total.reset_index()
    seasonly_total = seasonly_total.rename(columns={"total_count_hourly": "total_riders"})
    seasonly_total['season_daily'] = pd.Categorical(seasonly_total['season_daily'],
                                                   categories=['spring','summer','fall', 'winter'])
    seasonly_total = seasonly_total.sort_values('season_daily')
    return seasonly_total

# Menghitung Total pengguna per Musim
seasonly_total = create_seasonly_total(bike_dataset.dropna())

# Monthly
def create_monthly_user(bike_dataset):
    monthly_user = bike_dataset.resample(rule='M', on='date_day').agg({"total_count_hourly": "sum"})
    monthly_user.index = monthly_user.index.strftime('%b-%y')
    monthly_user = monthly_user.reset_index()
    monthly_user.rename(columns={
        "date_day": "month",
        "total_count_hourly": "total_riders",
    }, inplace=True)
    
    return monthly_user

# Menghitung Total Pengguna per Bulan
monthly_user = create_monthly_user(bike_dataset.dropna())

# Menampilkan Bar Chart Total Pengguna per Cuaca
fig = px.bar(weather_total, x="weather_daily", y="total_riders", title="Total Pengguna Sepeda per Cuaca")
st.plotly_chart(fig)

# Menampilkan Bar Chart Total Pengguna per Musim
fig = px.bar(seasonly_total, x="season_daily", y="total_riders", title="Total Pengguna Sepeda per Musim")
st.plotly_chart(fig)

# Menampilkan Line Chart Total Pengguna per Bulan
fig = px.line(monthly_user, x='month', y='total_riders', markers=True, title="Total Penyewaan Sepeda per Bulan")
st.plotly_chart(fig, use_container_width=True)

# Sidebar
st.sidebar.header("Visit my Profile:")
st.sidebar.markdown("Muhammad Faqih Maulana")

col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.markdown('<a href="https://www.linkedin.com/in/faqhmlna/"><img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" width="70"></a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="https://github.com/faqhmln?tab=repositories"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="60"></a>', unsafe_allow_html=True)
with col3:
    st.markdown('<a href="https://www.instagram.com/faqhmlna_/"><img src="https://static.xx.fbcdn.net/rsrc.php/v3/yx/r/tBxa1IFcTQH.png" width="60"></a>', unsafe_allow_html=True)

# Copyright(footer)
st.caption('Copyright ©, created by Muhammad Faqih Maulana')