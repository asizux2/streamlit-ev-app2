import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(page_title='Electric Vehicle Population Analysis', page_icon='🚗')
st.title('🚗 Electric Vehicle Population Analysis')

with st.expander('About this app'):
    st.markdown('**What can this app do?**')
    st.info('This app demonstrates the analysis of the electric vehicle population, leveraging Pandas for data manipulation and Altair for visualization.')
    st.markdown('**How to use the app?**')
    st.warning('To interact with the app, select vehicle makes of interest from the multi-select box and specify a range of years using the slider. This will update the displayed data frame and generate a corresponding line plot reflecting the total count or other metrics of selected electric vehicles over the specified years.')

st.subheader('Analyzing Electric Vehicle Population by Make and Year')

# Load data
@st.cache
def load_data():
    # Placeholder for actual CSV file path
    file_path = 'data/Electric_Vehicle_Population_Data.csv'
    data = pd.read_csv(file_path)
    # Ensure 'Year' is of type int for consistent slider behavior
    data['Year'] = data['Year'].astype(int)
    return data

df = load_data()

# Input widgets
## Make selection
makes_list = df['Make'].unique()
makes_selection = st.multiselect('Select Makes:', makes_list, default=['Tesla', 'Nissan'])

## Year selection
year_min, year_max = df['Year'].min(), df['Year'].max()
year_selection = st.slider('Select Year Range:', year_min, year_max, (year_min, year_max))

# Data filtering based on selection
df_filtered = df[(df['Make'].isin(makes_selection)) & (df['Year'].between(*year_selection))]

# Pivot for visualization
df_pivot = df_filtered.pivot_table(index='Year', columns='Make', values='Count', aggfunc='sum', fill_value=0)

# Display DataFrame
st.data_frame(df_pivot)

# Data preparation for Altair chart
df_chart = pd.melt(df_pivot.reset_index(), id_vars='Year', var_name='Make', value_name='Count')

# Display chart
chart = alt.Chart(df_chart).mark_line().encode(
    x='Year:O',
    y='Count:Q',
    color='Make:N',
    tooltip=['Year', 'Make', 'Count']
).interactive().properties(height=400)

st.altair_chart(chart, use_container_width=True)

st.markdown('**Note:** The line chart visualizes the yearly distribution of selected electric vehicle makes based on the user\'s selection, providing insights into trends over the selected time period.')
