

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ranked by Design & Style", layout="wide")

# Load and clean data

def load_data():
    df = pd.read_csv("credits.csv")
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('#', 'num')
    score_cols = ['Airtime', 'Speed', 'Pacing', 'First_Drop/Launch', 'Smoothness', 'Intensity', 'Overall']
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df, score_cols

df, score_cols = load_data()

st.title("🌀 Ranked by Design & Style")

# Group by Design type
if 'Design' in df.columns:
    st.subheader("🎢 Average Score by Coaster Design")
    design_avg = df.groupby("Design")[score_cols].mean().round(2)
    design_avg['Overall_Avg'] = df.groupby("Design")['Overall'].mean().round(2)
    design_avg = design_avg.sort_values("Overall_Avg", ascending=False)
    st.dataframe(design_avg)

    st.bar_chart(design_avg["Overall_Avg"])

# Group by Style type
if 'Style' in df.columns:
    st.subheader("🎠 Average Score by Coaster Style")
    style_avg = df.groupby("Style")[score_cols].mean().round(2)
    style_avg['Overall_Avg'] = df.groupby("Style")['Overall'].mean().round(2)
    style_avg = style_avg.sort_values("Overall_Avg", ascending=False)
    st.dataframe(style_avg)

    st.bar_chart(style_avg["Overall_Avg"])

# Best coaster in each design/style
if 'Design' in df.columns:
    st.subheader("🏆 Best Coaster in Each Design Type")
    top_by_design = df.loc[df.groupby('Design')['Overall'].idxmax()]
    st.dataframe(top_by_design[['Design', 'Name', 'Park', 'Overall']].sort_values('Overall', ascending=False))

if 'Style' in df.columns:
    st.subheader("🏅 Best Coaster in Each Style")
    top_by_style = df.loc[df.groupby('Style')['Overall'].idxmax()]
    st.dataframe(top_by_style[['Style', 'Name', 'Park', 'Overall']].sort_values('Overall', ascending=False))