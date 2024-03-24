
import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the Streamlit app
st.title('Electric Vehicle Population Analysis')

# Function to load the dataset
@st.cache
def load_data():
    # Placeholder file path - Update with the actual path to your CSV file
    file_path = r"C:\Users\khes7001\Desktop\DS Data\EV_Deploy\git\streamlit-ev-app\data\Electric_Vehicle_Population_Data.csv"
    data = pd.read_csv(file_path)
    return data

# Load the data using the defined function
ev_data = load_data()

# Display the first few rows of the dataframe
st.header('Dataset Overview')
st.write(ev_data.head())

# Sidebar widget for selecting 'Make'
make_selection = st.sidebar.multiselect('Select Make:', ev_data['Make'].unique())

# Filtering the dataframe based on the sidebar selection
if make_selection:
    filtered_data = ev_data[ev_data['Make'].isin(make_selection)]
    # Displaying filtered dataframe
    st.write(filtered_data)

# Example visualization: Count of Electric Vehicles by Make
if make_selection:
    make_counts = filtered_data['Make'].value_counts().reset_index()
    make_counts.columns = ['Make', 'Count']
    fig = px.bar(make_counts, x='Make', y='Count', title='Count of Electric Vehicles by Make')
    st.plotly_chart(fig)

# Additional sections for Electric Range Analysis, Correlation Analysis, etc., can be added here
