
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
import overview  # Importing the overview module

# Function to display the sidebar and handle navigation
def show_sidebar():
    page = st.sidebar.selectbox("Choose a page", ["Overview", "Another Page"])
    if page == "Overview":
        overview.display()  # Calling the display function from overview.py
    elif page == "Another Page":
        st.write("Content for another page.")

# Main function to run the app
def main():
    st.sidebar.title("Navigation")
    show_sidebar()

if __name__ == "__main__":
    main()

#################
 # Display dataset information
    st.header("Dataset Information")
    st.write("Total number of vehicles:", len(ev_data))
    st.dataframe(ev_data.head())

    # Make distribution analysis
    st.header("Make Distribution Analysis")
    make_counts = ev_data['Make'].value_counts()
    make_percentage = (make_counts / len(ev_data)) * 100
    make_counts_df = make_counts.reset_index()
    make_counts_df.columns = ['Make', 'Count']

    # Bar Chart for Make Counts
    fig_bar = px.bar(make_counts_df, x='Make', y='Count', title='Count of Electric Vehicles by Make',
                     color_discrete_sequence=px.colors.qualitative.Set2)
    fig_bar.update_layout(xaxis_title='Make', yaxis_title='Number of Vehicles', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_bar)

    # Pie Chart for Make Percentage
    fig_pie = px.pie(make_counts_df, names='Make', values='Count', title='Percentage Distribution of Electric Vehicles by Make',
                     color_discrete_sequence=px.colors.qualitative.Set3)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie)


