import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title='EV Range Analysis', page_icon='🔋')

# Load data function with the specified path
@st.cache
def load_data():
    # Specified file path on your local machine
    file_path = r"C:\Users\khes7001\Desktop\DS Data\EV_Deploy\git\streamlit-ev-app\data\Electric_Vehicle_Population_Data.csv"
    data = pd.read_csv(file_path)
    return data

df = load_data()

# Calculate statistics for Electric Range by Make
make_stats = df.groupby('Make')['Electric Range'].agg(['mean', 'std', 'min', 'max', 'count']).reset_index()

# Streamlit app layout
st.title('Electric Vehicle Range Analysis by Make')

# Mean Electric Range by Make
fig_mean = px.bar(make_stats, x='Make', y='mean', title='Mean Electric Range by Make')
st.plotly_chart(fig_mean)

# Standard Deviation of Electric Range by Make
fig_std = px.bar(make_stats, x='Make', y='std', title='Standard Deviation of Electric Range by Make')
st.plotly_chart(fig_std)

# Minimum Electric Range by Make
fig_min = px.bar(make_stats, x='Make', y='min', title='Minimum Electric Range by Make')
st.plotly_chart(fig_min)

# Maximum Electric Range by Make
fig_max = px.bar(make_stats, x='Make', y='max', title='Maximum Electric Range by Make')
st.plotly_chart(fig_max)

# Count of Vehicles by Make
fig_count = px.bar(make_stats, x='Make', y='count', title='Count of Vehicles by Make')
st.plotly_chart(fig_count)
