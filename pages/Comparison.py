import streamlit as st
import pandas as pd



@st.cache_data(ttl=300)  # Cache it for 5 minutes
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
    
st.subheader(f"📊 Compare Coasters")
compare_names = st.multiselect("Choose up to 3 Coasters to compare.", df['Name'].dropna().unique(), max_selections=3)
if compare_names:
    comparison = df[df['Name'].isin(compare_names)].set_index("Name")[score_cols]
    st.subheader("🧮 Comparison Table")
    st.dataframe(comparison.T)