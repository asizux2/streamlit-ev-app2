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
    ev_data = pd.read_csv(file_path)

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
            ev_data[column] = generator(len(ev_data))
    
    return ev_data

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
if 'Model Year' in df.columns and 'Electric Range' in df.columns:
    yearly_growth = df.groupby('Model Year').agg({'Electric Range': ['mean', 'count']}).reset_index()
    yearly_growth.columns = ['Model Year', 'Average Electric Range', 'Count']
    fig_3d_line = px.line_3d(yearly_growth, x='Model Year', y='Average Electric Range', z='Count', title='3D Line Chart: Yearly Growth of EV Adoption')
    st.plotly_chart(fig_3d_line)
else:
    missing_cols = {'Model Year', 'Electric Range'} - set(df.columns)
    st.error(f"Error: Missing necessary columns for the 3D Line Chart: {', '.join(missing_cols)}.")


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




# Display the first few rows and dataset information

display(ev_data.head())
ev_data.info()
ev_data['Model Year'] = ev_data['Model Year'].astype(str)
ev_data_cleaned = ev_data.dropna()
ev_data_cleaned.reset_index(drop=True, inplace=True)
ev_data_cleaned.set_index('VIN (1-10)', inplace=True)
make_counts = ev_data_cleaned['Make'].value_counts()
total_vehicles = make_counts.sum()
make_percentage = (make_counts / total_vehicles) * 100
make_percentage_df = make_percentage.reset_index()
make_percentage_df.columns = ['Make', 'Percentage']
make_percentage_df
make_counts_df = make_counts.reset_index()
make_counts_df.columns = ['Make', 'Count']
make_stats = ev_data_cleaned.groupby('Make')['Electric Range'].agg(['mean', 'std', 'min', 'max', 'count'])
ev_data_with_range = ev_data_cleaned[ev_data_cleaned['Electric Range'] > 0]
make_stats2 = ev_data_with_range.groupby('Make')['Electric Range'].agg(['mean', 'std', 'min', 'max', 'count'])
make_stats2

# Create a bar chart
fig = px.bar(make_counts_df, x='Make', y='Count', title='Count of Electric Vehicles by Make')
fig.update_layout(xaxis_title='Make', yaxis_title='Number of Vehicles', xaxis={'categoryorder':'total descending'})
fig.show()



# Create a pie chart
fig = px.pie(make_percentage_df, names='Make', values='Percentage', title='Percentage Distribution of Electric Vehicles by Make')
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()
make_stats = ev_data_cleaned.groupby('Make')['Electric Range'].agg(['mean', 'std', 'min', 'max', 'count'])

#Mean Electric Range by Make
fig_height = max(600, 20 * len(make_stats2.index))
fig_mean = px.bar(make_stats2.sort_values('mean', ascending=False).reset_index(), 
                  x='mean', y='Make', orientation='h', text='mean',
                  color='Make', title='Mean Electric Range by Make',
                  height=fig_height, width=800)
fig_mean.update_traces(texttemplate='%{text:.2f}', textposition='inside', marker_line_color='rgb(8,48,107)')
fig_mean.update_layout(xaxis_title='Mean Electric Range', yaxis_title='Make', showlegend=False)
fig_mean.show()

# Distribution of 'Electric Range' using a histogram
fig_range = px.histogram(ev_data_cleaned, x='Electric Range', title='Distribution of Electric Range')
fig_range.show()

# Scatter plot of 'Base MSRP' vs 'Electric Range'
fig_scatter = px.scatter(ev_data_cleaned, x='Base MSRP', y='Electric Range', color='Make', title='Base MSRP vs Electric Range by Make')
fig_scatter.show()

# Box plot of 'Electric Range' by 'Make'
fig_box = px.box(ev_data_cleaned, x='Make', y='Electric Range', title='Electric Range by Make')
fig_box.show()

# Violin plot of 'Electric Range' by 'Make'
fig_violin = px.violin(ev_data_cleaned, x='Make', y='Electric Range', box=True, title='Electric Range Distribution by Make')
fig_violin.show()

#Correlation Matrix using imshow
corr_matrix = ev_data_cleaned.select_dtypes(include=[np.number]).corr()
corr_matrix_rounded = corr_matrix.round(2)
fig_imshow = px.imshow(corr_matrix_rounded, text_auto=True, aspect='auto', title='Correlation Matrix using imshow')
fig_imshow.update_xaxes(side='top')
fig_imshow.show()




