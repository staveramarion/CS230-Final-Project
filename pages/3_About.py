"""
About page --> Overview of the project
"""

import streamlit as st
st.set_page_config(page_title="About",page_icon="ℹ️",layout="wide")
st.title("About this project")

st.write("""
This is my CS 230 final project, by Sofia Tavera.

I chose the Blue Bikes Boston dataset beacuse I was curious about how people are able to
explore a city on bikes. Especially since this dataset was during the early pandemic, when biking became
a huge trend.
""")

st.header("What I built")
st.write("""
Streamlit multipage app, which has three pages:

- HOME: sidebar filters, rider types, hour of the day, day of the week
and time of the day, summary metrics.
- WHEN: trip duration histogram and a heatmap that shows what people
are riding by the hour and day of the week.
- WHERE: bar chart of the busiest stations, PyDeck map that has hover 
tooltips, Folium map with clickable popups.
""")

st.header("What I learned")
st.write("""
- Pandas pivot tables are essential when you want to summarize data.
- Folium provides clickable map markers, since the built in maps by Streamlit
 does not. Used for extra credit since we did not cover in class.
- Theme changes need a full restart.
""")

st.header("AI use")
st.write("""
I used AI to help me with the more advances coding,and as a guide when setting up the multi-page Streamlit structure
""")