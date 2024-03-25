import streamlit as st
import pandas as pd
import plotly.express as px

# Set the Mapbox access token for geographic visualizations
px.set_mapbox_access_token('sk.eyJ1IjoiZXNsNG1raDRsZWQiLCJhIjoiY2x1NmVnb2plMXpzeDJtbnh4eHNxZWF0dyJ9.q5VUpwvtE5nlw31bg_QHHg')

# Function to load and cache data
@st.cache
def load_data():
    file_path = r"C:\Users\khes7001\Desktop\DS Data\EV_Deploy\git\streamlit-ev-app\data\Electric_Vehicle_Population_Data.csv"  # Update with your actual data path
    data = pd.read_csv(file_path)
    return data

# Function to extract latitude and longitude from "Vehicle Location"
def extract_coordinates(df):
    coords = df['Vehicle Location'].str.extract(r'POINT \(([^ ]+) ([^ ]+)\)')
    df['Longitude'] = coords[0].astype(float)
    df['Latitude'] = coords[1].astype(float)
    return df

# Load the data
df = load_data()

# Data Overview
st.markdown("## Data Overview")
st.write(df.head())

# EV Adoption Rate
ev_growth = df.groupby('Model Year').size().reset_index(name='Count')
fig_adoption = px.line(ev_growth, x='Model Year', y='Count', title='EV Adoption Over Years')
st.plotly_chart(fig_adoption)

# Market Diversity
market_diversity = df.groupby('Model Year')['Make'].nunique().reset_index(name='Unique Makes')
fig_diversity = px.line(market_diversity, x='Model Year', y='Unique Makes', title='Market Diversity Over Years')
st.plotly_chart(fig_diversity)

# Range Improvement
range_improvement = df.groupby('Model Year')['Electric Range'].mean().reset_index()
fig_range_improvement = px.line(range_improvement, x='Model Year', y='Electric Range', title='Average Electric Range Improvement Over Years')
st.plotly_chart(fig_range_improvement)

# Price vs. Range
fig_price_range = px.scatter(df, x='Base MSRP', y='Electric Range', color='Model Year', trendline='ols', title='Price vs. Electric Range Over Years')
st.plotly_chart(fig_price_range)

# Model Popularity
popular_models = df['Model'].value_counts().head(10).reset_index()
popular_models.columns = ['Model', 'Count']
fig_popularity = px.bar(popular_models, x='Model', y='Count', title='Top 10 Popular EV Models')
st.plotly_chart(fig_popularity)

# Extract coordinates for geographic visualization
df = extract_coordinates(df)

# Geographic Distribution Visualization
st.markdown("## Geographic Distribution of EVs")
fig_geo = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Model", color_discrete_sequence=["fuchsia"], zoom=3)
fig_geo.update_layout(mapbox_style="light", margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_geo)
