"""
Where does Boston ride? --> top stations bar chart and the Pydeck map
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Where | Blue Bikes", page_icon="📍", layout="wide")

@st.cache_data
def load_data(path, sample_frac=1.0):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Could not find {path}")
        return pd.DataFrame()

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df["starttime"] = pd.to_datetime(df["starttime"], errors="coerce")
    df = df.dropna(subset=["starttime"])
    df["trip_minutes"] = df["tripduration"] / 60
    df["hour"] = df["starttime"].dt.hour
    df["day_of_week"] = df["starttime"].dt.day_name()
    df = df[df["trip_minutes"] <= 180]

    if sample_frac < 1.0:
        df = df.sample(frac=sample_frac, random_state=42)

    return df

df = load_data("202009-bluebikes-tripdata.csv")

st.title("Where does Boston ride?")
st.write("This page shows the busiest stations and a map of where the trips start!")

# Chart 1 --> top stations bar chart
st.header("Top starting stations")
# showing how many to show
n_stations = st.slider("How many stations to show?", 5, 25, 10)
# [DA3] top N largest values
# [DA2] sprt by descending
top = df["start_station_name"].value_counts().head(n_stations).sort_values()
# [VIZ1] horizontal bar chart i put custom colors and title
fig, ax = plt.subplots(figsize=(8,6))
ax.barh(top.index, top.values, color="#0B3D91")
ax.set_xlabel("Number of trips")
ax.set_title(f"Top {n_stations} starting stations")
plt.tight_layout()

st.pyplot(fig)

# Map
st.header("Where are the busiest stations?")
# [DA7] to create new columns by grouping
station_counts = df.groupby(["start_station_name", "start_station_latitude","start_station_longitude"]).size().reset_index(name="trips")
# only have top stations so that the map is clean
station_counts = station_counts.nlargest(50, "trips")
# [DA3] top N
# Top 5 stations
st.header("Top 5 stations breakdown")
top5 = station_counts.head(5)
# [DA8] iterate through DataFrame rows
for index, row in top5.iterrows():
    st.write(f"**{row['start_station_name']}** - {row['trips']:,} trips")

# Map Pydeck scatterplot
layer = pdk.Layer("ScatterplotLayer", data=station_counts, get_position =["start_station_longitude","start_station_latitude"], get_radius="trips /50", get_fill_color= [11,61,145,200],pickable=True,
)
view_state = pdk.ViewState(latitude=42.355, longitude=-71.085,zoom=12,
)
deck = pdk.Deck(layers=[layer],initial_view_state=view_state, tooltip={"text": "{start_station_name}\n{trips} trips"}, map_style="light",
)
st.pydeck_chart(deck)


# Folium map --> we did not use in class
st.header("Folium map of top stations")
st.write ("Click a circle to see the station name and trip count.")

# creating a base map centered on Boston
m = folium.Map(location=[42.355, -71.085], zoom_start=13)
# adding a marker for each top station
# [DA8] iterate through the dataframe wors with iterrows()
for index, row in station_counts.iterrows():
    folium.CircleMarker(location=[row["start_station_latitude"], row["start_station_longitude"]],
                        radius=row["trips"]/500, popup=f"{row['start_station_name']}: {row['trips']:,} trips", color="darkblue",
                        fill=True,fillOpacity=0.6,).add_to(m)
# render inside streamlit
st_folium(m, width=700, height=500, returned_objects=[])

