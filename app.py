import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set the Mapbox access token for geographic visualizations
px.set_mapbox_access_token('sk.eyJ1IjoiZXNsNG1raDRsZWQiLCJhIjoiY2x1NmVnb2plMXpzeDJtbnh4eHNxZWF0dyJ9.q5VUpwvtE5nlw31bg_QHHg')

# Function to load and cache data
@st.cache
def load_data():
    file_path = r"C:\Users\khes7001\Desktop\DS Data\EV_Deploy\git\streamlit-ev-app\data\Electric_Vehicle_Population_Data.csv"  # Update with your actual data path
    data = pd.read_csv(file_path)

    # Enriching the dataset with necessary columns and random data
    necessary_columns = {
        'Model Year': lambda n: np.random.randint(2000, 2023, n),
        'Make': lambda n: np.random.choice(['Tesla', 'Nissan', 'Chevrolet', 'Ford', 'BMW'], n),
        'Electric Range': lambda n: np.random.randint(50, 400, n),
        'Base MSRP': lambda n: np.random.randint(30000, 120000, n),
        'Battery Capacity': lambda n: np.random.uniform(20, 100, n).round(2),
        'State': lambda n: np.random.choice(['CA', 'TX', 'NY', 'FL', 'WA'], n),
        'Vehicle Location': lambda n: ["POINT ({:.6f} {:.6f})".format(np.random.uniform(-125, -66), np.random.uniform(24, 49)) for _ in range(n)]
    }

    for column, generator in necessary_columns.items():
        if column not in data.columns:
            data[column] = generator(len(data))
    
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
fig_price_range = px.scatter(df, x='Base MSRP', y='Electric Range', color='Model Year', title='Price vs. Electric Range Over Years')
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


# Yearly Growth Rate
ev_growth = df.groupby('Model Year').size()
yearly_growth_rate = ev_growth.pct_change() * 100  # Convert to percentage
fig_growth_rate = px.line(yearly_growth_rate.reset_index(), x='Model Year', y=0, labels={'0': 'Growth Rate (%)'}, title='Yearly EV Population Growth Rate')
fig_growth_rate.update_layout(yaxis_tickformat='%')  # Display y-axis values as percentages
st.plotly_chart(fig_growth_rate)



# Range vs. Battery Capacity
fig_range_battery = px.scatter(df, x='Battery Capacity', y='Electric Range', color='Make', title='Range vs. Battery Capacity by Make')
fig_range_battery.update_layout(xaxis_title='Battery Capacity (kWh)', yaxis_title='Electric Range (miles)')
st.plotly_chart(fig_range_battery)

# 3D Line Chart: Yearly Growth of EV Adoption in 3D
yearly_growth = df.groupby('Model Year').agg({'Electric Range': 'mean', 'VIN': 'count'}).reset_index()
yearly_growth.columns = ['Model Year', 'Average Electric Range', 'Count']
fig_3d_line = px.line_3d(yearly_growth, x='Model Year', y='Average Electric Range', z='Count', title='3D Line Chart: Yearly Growth of EV Adoption')
st.plotly_chart(fig_3d_line)


# 3D Surface Plot: Battery Capacity vs. Electric Range Surface
# Assuming an aggregated or sampled dataset for surface plotting
#fig_3d_surface = px.scatter_3d(df, x='Battery Capacity', y='Electric Range', z='Model Year', color='Electric Range', title='Battery Capacity vs. Electric Range Surface')
#fig_3d_surface.update_traces(type='surface')
#st.plotly_chart(fig_3d_surface)

# Heatmap: Model Year vs. Make Count
heatmap_data = df.groupby(['Model Year', 'Make']).size().unstack(fill_value=0)
fig_heatmap = px.imshow(heatmap_data, labels=dict(x="Make", y="Model Year", color="Count"), title='Model Year vs. Make Count')
st.plotly_chart(fig_heatmap)

#Contour Plot: Density of Electric Range and MSRP
fig_contour = px.density_contour(df, x='Electric Range', y='Base MSRP', title='Contour Plot: Density of Electric Range and MSRP')
st.plotly_chart(fig_contour)

#Polar Chart: Average Electric Range by State
avg_range_by_state = df.groupby('State')['Electric Range'].mean().reset_index()
fig_polar = px.line_polar(avg_range_by_state, r='Electric Range', theta='State', line_close=True, title='Polar Chart: Average Electric Range by State')
st.plotly_chart(fig_polar)



