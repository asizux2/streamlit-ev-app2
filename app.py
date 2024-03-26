import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set the Mapbox access token for geographic visualizations
px.set_mapbox_access_token('YOUR_MAPBOX_ACCESS_TOKEN')

# Function to load and cache data
@st.cache
def load_data():
    # Update with your actual data path
    file_path = r"C:\Users\khes7001\Desktop\DS Data\EV_Deploy\git\streamlit-ev-app\data\Electric_Vehicle_Population_Data.csv"
    df = pd.read_csv(file_path)
    
    # Simulate additional necessary columns if they don't exist in your CSV
    for column in ['Model Year', 'Make', 'Electric Range', 'Base MSRP', 'Battery Capacity', 'State', 'Vehicle Location']:
        if column not in df.columns:
            df[column] = np.nan  # Placeholder for non-existent columns
    
    return df

df = load_data()

# Convert 'Model Year' to string
df['Model Year'] = df['Model Year'].astype(str)

# Clean data
df_cleaned = df.dropna()
df_cleaned.reset_index(drop=True, inplace=True)

# Vehicle make counts and percentages
make_counts = df_cleaned['Make'].value_counts()
make_percentage = (make_counts / make_counts.sum()) * 100

# Bar Chart: Count of Electric Vehicles by Make
fig_bar = px.bar(make_counts.reset_index(), x='index', y='Make', title='Count of Electric Vehicles by Make')
fig_bar.update_layout(xaxis_title='Make', yaxis_title='Number of Vehicles', xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig_bar)

# Pie Chart: Percentage Distribution of Electric Vehicles by Make
fig_pie = px.pie(make_percentage.reset_index(), names='index', values='Make', title='Percentage Distribution of Electric Vehicles by Make')
fig_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_pie)

# Prepare data for mean electric range by make
df_with_range = df_cleaned[df_cleaned['Electric Range'] > 0]
make_stats = df_with_range.groupby('Make')['Electric Range'].agg(['mean', 'std', 'min', 'max', 'count']).reset_index()

# Bar Chart: Mean Electric Range by Make
fig_mean_range = px.bar(make_stats.sort_values('mean', ascending=False), 
                        x='mean', y='Make', orientation='h', text='mean',
                        color='Make', title='Mean Electric Range by Make')
fig_mean_range.update_traces(texttemplate='%{text:.2f}', textposition='inside')
fig_mean_range.update_layout(xaxis_title='Mean Electric Range', yaxis_title='Make', showlegend=False)
st.plotly_chart(fig_mean_range)

# Histogram: Distribution of Electric Range
fig_histogram = px.histogram(df_cleaned, x='Electric Range', title='Distribution of Electric Range')
st.plotly_chart(fig_histogram)

# Scatter Plot: Base MSRP vs Electric Range
fig_scatter = px.scatter(df_cleaned, x='Base MSRP', y='Electric Range', color='Make', title='Base MSRP vs Electric Range by Make')
st.plotly_chart(fig_scatter)

# Box Plot: Electric Range by Make
fig_box = px.box(df_cleaned, x='Make', y='Electric Range', title='Electric Range by Make')
st.plotly_chart(fig_box)

# Violin Plot: Electric Range Distribution by Make
fig_violin = px.violin(df_cleaned, x='Make', y='Electric Range', box=True, title='Electric Range Distribution by Make')
st.plotly_chart(fig_violin)

# Correlation Matrix using imshow
corr_matrix = df_cleaned.select_dtypes(include=[np.number]).corr().round(2)
fig_imshow = px.imshow(corr_matrix, text_auto=True, aspect='auto', title='Correlation Matrix')
fig_imshow.update_xaxes(side='top')
st.plotly_chart(fig_imshow)


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
if 'Model Year' in df.columns and 'Electric Range' in df.columns:
    yearly_growth = df.groupby('Model Year').agg({'Electric Range': ['mean', 'count']}).reset_index()
    yearly_growth.columns = ['Model Year', 'Average Electric Range', 'Count']
    fig_3d_line = px.line_3d(yearly_growth, x='Model Year', y='Average Electric Range', z='Count', title='3D Line Chart: Yearly Growth of EV Adoption')
    st.plotly_chart(fig_3d_line)
else:
    missing_cols = {'Model Year', 'Electric Range'} - set(df.columns)
    st.error(f"Error: Missing necessary columns for the 3D Line Chart: {', '.join(missing_cols)}.")



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




