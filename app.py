import streamlit as st
import pandas as pd


"""higher lower game trivia about roller coasters
This app allows users to explore roller coaster data, filter by park and manufacturer,
most wanted list/most anticipated
rate roller coasters based on various attributes, and compare them visually.
rate roller coasters by manufacturers"""


  # Cache it for 5 minutes
def load_data():
    df = pd.read_csv("credits.csv")
    return df

df = load_data()
# Rename and clean column names
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('#', 'num')

# Convert scores to numeric
score_cols = ['Airtime', 'Speed', 'Pacing', 'First_Drop/Launch', 'Smoothness', 'Intensity', 'Overall']
for col in score_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    
    
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


st.subheader(f"📊 Compare Coasters")
compare_names = st.multiselect("Choose up to 3 Coasters to compare.", df['Name'].dropna().unique(), max_selections=3)
if compare_names:
    comparison = df[df['Name'].isin(compare_names)].set_index("Name")[score_cols]
    st.subheader("🧮 Comparison Table")
    st.dataframe(comparison.T)

#st.title("🎢 Dave's Dashboard")
#st.dataframe(df)