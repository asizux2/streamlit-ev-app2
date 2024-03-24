
import streamlit as st
import pandas as pd
import plotly.express as px

def display():
    st.title("Electric Vehicle Population Overview")

    # Introduction
    st.write("""
    This overview provides insights into the Electric Vehicle Population, 
    highlighting key statistics and distributions among vehicle makes.
    """)

    # Load data (adjust the file path as needed)
    @st.cache
    def load_data():
        file_path = r"C:\Users\khes7001\Desktop\DS Data\EV_Deploy\git\streamlit-ev-app\data\Electric_Vehicle_Population_Data.csv"  # Update this path
        data = pd.read_csv(file_path)
        return data

    ev_data = load_data()

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
