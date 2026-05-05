"""
When does Boston ride? ==== Duration histogram and hour/day heatmap
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# this page shows own page configuration
st.set_page_config(page_title="When | Blue Bikes", page_icon="⏰", layout="wide")

def load_data(path, max_minutes=180):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Could not find {path}")
        return pd.DataFrame()

    new_columns = []
    for col in df.columns:
        new_columns.append(col.lower())
    df.columns = new_columns

    df["starttime"] = pd.to_datetime(df["starttime"], errors="coerce")
    df = df.dropna(subset=["starttime"])
    df["trip_minutes"] = df["tripduration"] / 60
    df["hour"] = df["starttime"].dt.hour
    df["day_of_week"] = df["starttime"].dt.day_name()
    df = df[df["trip_minutes"] <= max_minutes]


    return df


df = load_data("202009-bluebikes-tripdata.csv")
st.title("When does Boston ride?")
st.write("This page explores when Boston rides, by trip duration and time of the day")

# Chart 2: trip duration histogram
st.header("How long are trips?")
# [VIZ2] histogram, limited at 60 minutes
limited = df[df["trip_minutes"] <= 60]
fig2, ax2 = plt.subplots(figsize=(9,4))
ax2.hist(limited["trip_minutes"],bins=40, color="#F4A261", edgecolor="white")
ax2.set_xlabel("Trip duration (minutes)")
ax2.set_ylabel("Number of trips")
ax2.set_title("Trip duration distribution")
plt.tight_layout()

st.pyplot(fig2)
st.write(f"Median trip length: {df['trip_minutes'].median():.1f} minutes")

# Chart 3: pivot table by hour and day
st.header("When do people ride?")
# [DA6] pivot table
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = df.pivot_table( index= "day_of_week", columns= "hour", values = "trip_minutes", fill_value=0).reindex(day_order)
# [VIZ3] heatmap from the pivot table
fig3, ax3 = plt.subplots(figsize=(11,4))
im = ax3.imshow(pivot.values, cmap= "YlGnBu")
ax3.set_xticks(range(24))
ax3.set_xticklabels(range(24))
ax3.set_yticks(range(7))
ax3.set_yticklabels(day_order)
ax3.set_xlabel("Hour of day")
ax3.set_title("Average trip duration by day and hour")
fig3.colorbar(im, ax=ax3, label="Average minutes")
plt.tight_layout()

st.pyplot(fig3)



