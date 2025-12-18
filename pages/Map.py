import streamlit as st
import pandas as pd

@st.cache_data(ttl=300)  # Cache it for 5 minutes
def load_data():
    df = pd.read_csv("/Users/larryontruman/Desktop/Coding/5_Experiments/dave-roller/Roller Coaster Credits - Davids Credit Count.csv")
    return df

df = load_data()
# Rename and clean column names
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('#', 'num')

# Convert scores to numeric
score_cols = ['Airtime', 'Speed', 'Pacing', 'First_Drop/Launch', 'Smoothness', 'Intensity', 'Overall']
for col in score_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Add latitude and longitude for park mapping
park_locations = {
    "Universal's Island of Adventure": (28.4718, -81.4734),
    "Cedar Point": (41.4822, -82.6835),
    "Busch Gardens Williamsburg": (37.2340, -76.6469),
    "Six Flags Great Adventure": (40.1369, -74.4408),
    "Busch Gardens Tampa Bay": (28.0336, -82.4194),
    "Walt Disney World": (28.3852, -81.5639),
    "Kings Dominion": (37.8390, -77.4436),
    "Kings Island": (39.3440, -84.2700),
    "Universal Studios, FL": (28.4743, -81.4678),
    "Hershey Park": (40.2883, -76.6544),
    "Sea World San Diego": (32.7648, -117.2266),
    "Sea World Orlando": (28.4115, -81.4625),
    "Dorney Park": (40.5790, -75.5176),
    "Mt. Olympus": (43.5738, -89.7764),
}

# Create a new DataFrame from the park_locations dictionary
location_df = pd.DataFrame([
    {'Park': park, 'LAT': lat, 'Longitude': lon}
    for park, (lat, lon) in park_locations.items()
])

# Merge it with the main DataFrame
df = df.merge(location_df, on='Park', how='left')


# Sidebar filters
st.sidebar.header("🔎 Filter Coasters")

selected_park = st.sidebar.multiselect("Park", sorted(df['Park'].dropna().unique()))
selected_make = st.sidebar.multiselect("Manufacturer", sorted(df['Make'].dropna().unique()))

filtered_df = df.copy()

if selected_park:
    filtered_df = filtered_df[filtered_df['Park'].isin(selected_park)]
if selected_make:
    filtered_df = filtered_df[filtered_df['Make'].isin(selected_make)]

st.title("🎢 Dave's Dashboard")

# Show map of coaster parks if location data is available
if 'Latitude' in filtered_df.columns and 'Longitude' in filtered_df.columns:
    st.subheader("🗺️ Coaster Parks Map")
    st.map(filtered_df[['Latitude', 'Longitude']].dropna())

st.dataframe(filtered_df) 

st.subheader("⭐ Top 10 Coasters by Overall Score")
top_overall = filtered_df.sort_values("Overall", ascending=False).head(10)
st.bar_chart(top_overall.set_index("Name")["Overall"])

st.subheader("🎯 Attribute Comparison")

attr = st.selectbox("Choose attribute to compare", score_cols)
st.bar_chart(filtered_df.set_index("Name")[attr].sort_values(ascending=False).head(10))

import plotly.express as px

top = filtered_df.sort_values("Overall", ascending=False).iloc[0]

st.subheader(f"🌟 Attribute Profile: {top['Name']}")

radar_df = pd.DataFrame({
    'Attribute': score_cols,
    'Score': [top[col] for col in score_cols]
})

fig = px.line_polar(radar_df, r='Score', theta='Attribute', line_close=True, title=f"{top['Name']} Profile")
st.plotly_chart(fig)

st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Total Coasters", len(df))
st.sidebar.metric("Unique Parks", df['Park'].nunique())
st.sidebar.metric("Top Manufacturer", df['Make'].mode()[0])

st.subheader("🏅 Top Coasters by Each Category")
for col in score_cols:
    top_ride = df.sort_values(col, ascending=False).iloc[0]
    st.write(f"**{col}**: {top_ride['Name']} ({top_ride['Park']}) — {top_ride[col]}")



#st.title("🎢 Dave's Dashboard")
#st.dataframe(df)