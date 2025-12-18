

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ranked by Make", layout="wide")

# Load and clean data

def load_data():
    df = pd.read_csv("credits.csv")
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('#', 'num')
    score_cols = ['Airtime', 'Speed', 'Pacing', 'First_Drop/Launch', 'Smoothness', 'Intensity', 'Overall']
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df, score_cols

df, score_cols = load_data()

st.title("🏭 Ranked by Manufacturer")

# Average scores per manufacturer
make_scores = df.groupby("Make")[score_cols].mean().round(2)
make_scores['Overall_Avg'] = df.groupby("Make")['Overall'].mean().round(2)
make_scores = make_scores.sort_values("Overall_Avg", ascending=False)

st.subheader("🏆 Average Score by Manufacturer")
st.dataframe(make_scores)

st.subheader("📊 Top Manufacturers by Overall Average")
st.bar_chart(make_scores["Overall_Avg"].head(10))

st.subheader("🎢 Number of Coasters per Manufacturer")
coaster_count = df['Make'].value_counts()
st.bar_chart(coaster_count)

st.subheader("🧠 Attribute Profile by Manufacturer")
selected_make = st.selectbox("Select a manufacturer", make_scores.index)

if selected_make:
    radar_df = make_scores.loc[[selected_make]].T.reset_index()
    radar_df.columns = ['Attribute', 'Score']
    radar_df = radar_df[radar_df['Attribute'].isin(score_cols)]
    fig = px.line_polar(radar_df, r='Score', theta='Attribute', line_close=True, title=f"{selected_make} Coaster Profile")
    st.plotly_chart(fig)

st.subheader("🏅 Best Coaster from Each Manufacturer")
top_by_make = df.loc[df.groupby('Make')['Overall'].idxmax()]
top_by_make = top_by_make[['Make', 'Name', 'Park', 'Overall']].sort_values('Overall', ascending=False)
st.dataframe(top_by_make)