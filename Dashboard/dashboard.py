import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import streamlit as st # type: ignore
sns.set(style='dark')

def get_count_by_hour_df(df):
    hour_count_df = df.groupby(by="hour").agg({"total_count": "sum"}).sort_values(by="total_count", ascending=False).head(5)
    return hour_count_df

def get_rent_month_df(df):
    month_count_df = df.groupby(by="month").total_count.sum().sort_values(ascending=False).reset_index()
    return month_count_df

def distrib_casual_df(df):
    casual_df = df.groupby(by="date").agg({"casual": ["sum"]}).reset_index()
    casual_df.columns = ['date', 'cas_sum']
    return casual_df

def distrib_registered_df(df):
    registered_df = df.groupby(by="date").agg({"registered": ["sum"]}).reset_index()
    registered_df.columns = ['date', 'regist_sum']
    return registered_df

def weather_rent_df(df):
    weather_df = df.groupby(by="weather").agg(total_weather=("total_count", "sum")).reset_index()
    return weather_df

def top5_hour_df(df):
    hour_df = df.groupby(by="hour").total_count.sum().sort_values(ascending=False).reset_index().head(5)
    return hour_df

def cluster_manual_df(df):
    cluster_df = df.groupby(['Day_Categories', 'weather']).agg({
    'temperature': 'mean',
    'humidity': 'mean',
    'windspeed': 'mean',
    'total_count': 'mean'}).reset_index()
    return cluster_df

# Membaca data dari file CSV
main_df = pd.read_csv("Dashboard/all_data.csv")

# Memanggil fungsi
casual_df = distrib_casual_df(main_df)
registered_df = distrib_registered_df(main_df)
hour_df = top5_hour_df(main_df)
month_count_df = get_rent_month_df(main_df)
weather_df = weather_rent_df(main_df)
cluster_df = cluster_manual_df(main_df)

image_path = "EDA-BikeSharing\Logo.jpg"

# Membuat tampilan sidebar
with st.sidebar:
    st.image(image_path)
    st.title("Bike Sharing Analysis :sparkles:")
    st.write("Explore the insights of bike sharing data, including usage patterns, weather conditions, and more.")
    st.markdown("### About this Board")
    st.write("This Dashboard provides an analysis of bike sharing data, helping users understand trends and patterns.")

# Membuat tampilan dashboard
st.header('----- Data Insight -----')

st.subheader('Daily Sharing')
col1, col2 = st.columns(2)
with col1:
    total_sum = casual_df.cas_sum.sum() 
    st.metric("Total Casual", value=total_sum)
with col2:
    total_registered_sum = registered_df.regist_sum.sum()
    st.metric("Total Registered", value=total_registered_sum)

# plot 1: hour
st.subheader("Best Hour for Bike Sharing")
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#D3D3D3", "#D3D3D3", "#00827f", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="hour", y="total_count", data=hour_df, palette=colors, ax=ax) 
ax.set_ylabel(None)
ax.set_xlabel("Hour", size=10)
ax.set_title(None)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig) 

# plot 2: top and low
st.subheader("Top and Lowest Bike Rentals by Month")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors = ["#00827f", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="total_count", y="month", data=month_count_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None, fontsize=25)  
ax[0].set_xlabel(None, fontsize=25)  
ax[0].set_title("Top Bike Rentals by Month", loc="center", fontsize=25)  
ax[0].tick_params(axis='y', labelsize=20)
sns.barplot(x="total_count", y="month", data=month_count_df.sort_values(by="total_count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None, fontsize=25)  
ax[1].set_xlabel(None, fontsize=25) 
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Lowest Bike Rentals by Month", loc="center", fontsize=25) 
ax[1].tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# plot 3: percentage casual vs registered
st.subheader("Percentage Casual vs Registered")
fig, ax = plt.subplots(figsize=(10, 5))
total_casual = casual_df.cas_sum.sum()
total_registered = registered_df.regist_sum.sum()
total_data = [total_casual, total_registered]
label_plt = ['Casual', 'Registered']
colors = ("#D3D3D3", "#00827f")
ax.pie(
    x=total_data,
    labels=label_plt,
    autopct='%1.1f%%',
    colors=colors,
    startangle=90
)
ax.set_title("Percentage of Casual vs Registered Users", fontsize=15)
ax.axis('equal')
st.pyplot(fig)

# plot 4: weather condition 
st.subheader("Best Weather for Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="total_weather", y="weather", data=weather_df.sort_values(by="total_weather", ascending=False), 
            palette=["#00827f", "#D3D3D3", "#D3D3D3"], ax=ax) 
ax.set_ylabel(None)
ax.set_xlabel("Total Count", fontsize=10)
ax.set_title(None)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig) 

# analisis lanjutan clustering
st.subheader("Average Bike Rentals by Day Type and Weather Conditions")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=cluster_df,
    x='Day_Categories',
    y='total_count',
    hue='weather',
    palette=["#00827f", "#5f9ea0", "#D3D3D3"],
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel("Day Type", fontsize=12)
ax.legend(title='Weather Condition', fontsize=10)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
plt.tight_layout() 
st.pyplot(fig)