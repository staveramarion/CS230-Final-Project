"""
Name: Sofia Tavera
CS230: Section 8
Data: Blue Bikes Boston Trips from September 2020
URL:

Description:
This app explores the Boston Blue Bikes trips starting from September 2020.
Usera are able to filter trips and see charts and maps.
"""

import streamlit as st
import pandas as pd

# [ST4] customizing page
st.set_page_config( page_title="Boston Blue Bikes", page_icon= "🚲", layout="wide", initial_sidebar_state="expanded")
# [PY1] function two parameters, default_age has a default value
@st.cache_data
def load_data(path, default_age = 2026):
    # [PY3] try/except for error checking
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Could not find {path}")
        return pd.DataFrame()
    # [DA1] clean columns names, making them lowercase with underscores
    df.columns = [c.strip().lower().replace(" ","_") for c in df.columns]
    # [DA1] parse the date columns
    df["starttime"] = pd.to_datetime(df["starttime"],errors="coerce")
    df = df.dropna(subset=["starttime"])
    # [DA9] add new columns from existing ones
    df["trip_minutes"] = df["tripduration"]/60
    df["hour"] = df["starttime"].dt.hour
    df["day_of_week"] = df["starttime"].dt.day_name()
    # [DA1] drop long trips (>3 hours)
    df = df[df["trip_minutes"] <= 180]

    return df


st.title("Boston Blue Bikes from September 2020")
df = load_data(r"C:\Users\sofia\PycharmProjects\PythonProject\PythonProject2\202009-bluebikes-tripdata.csv")

st.write(f"Loaded {len(df):,} trips.")
st.dataframe(df.head())

# SIDEBAR FILTERS
st.sidebar.header("Filters")
# [ST1] multiselect for rider type
user_types = st.sidebar.multiselect("Rider type", options= df["usertype"].unique(), default= df["usertype"].unique())
# [ST2] slider for hour of the day
hour_range = st.sidebar.slider("Hour of day (24-hour)", min_value= 0, max_value= 23, value=(0,23))
# [ST3] selectbox for the day of the week
day_filter = st.sidebar.selectbox("Day of week", options= ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])


# APPLYING THE FILTERS
# [DA5] filter with multiple and conditions
filtered = df[df["usertype"].isin(user_types) & df["hour"].between(hour_range[0],hour_range[1])]
# [DA4] add another single filter on the day of the week if not "ALL"
if day_filter != "All":
    filtered = filtered[filtered["day_of_week"] == day_filter]
st.write(f"Showing {len(filtered):,} of {len(df):,} trips.")

import matplotlib.pyplot as plt



# [PY5] dictionary mapping time of day labels to hour ranges
time_of_day_map = {"Morning Rush (5-10am)": (5,9), "Midday (10am-3pm)": (10, 14),"Evening Rush (3-7pm)": (15, 18), "Evening (7-11pm)": (19, 22), "Late Night (11pm-5am)": (23, 4),
}
# [PY4] list comprehension to build the option labels from the dictionary
time_labels = [label for label, hours in time_of_day_map.items()]
selected_times = st.sidebar.multiselect("Time of day", options=time_labels, default=time_labels)
# [PY5] read dictionary items to build a list of hours that match the selected periods
selected_hours = []
for label, hours in time_of_day_map.items():
    if label in selected_times:
        start, end = hours
        if start <= end:
            for i in range(start, end + 1):
                selected_hours.append(i)
        else:
            for i in range(start,24):
                selected_hours.append(i)
            for i in range(0, end +1):
                selected_hours.append(i)
if selected_hours:
    filtered = filtered[filtered["hour"].isin(selected_hours)]
# [PY2] function tht will return more than one value
def summary_stats(trips_df):
    total = len(trips_df)
    median_min = trips_df["trip_minutes"].median()
    n_stations = trips_df["start_station_name"].nunique()
    return total, median_min, n_stations
total, median_min, n_stations = summary_stats(filtered)
col1, col2, col3 =st.columns(3)
col1.metric("Total trips", f"{total:,}")
col2.metric("Median trip", f"{median_min:.1f} min")
col3.metric("Stations", n_stations)





