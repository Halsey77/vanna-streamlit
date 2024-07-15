import streamlit as st
import numpy as np
import pandas as pd

from vanna_calls import (import_new_data_and_train_cached)

st.set_page_config(page_title='Input data', layout='wide')

# Set up main page

st.markdown("# Input data")
st.write("In this page, you can input your data in the form of a CSV file. The data will be stored in a pandas DataFrame and displayed in a table below.")

# Create a file uploader to upload a CSV file
def file_uploader():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    
    return None

df = file_uploader()

# Display the data in a table
def display_data(df):
    if df is not None:
        st.write(df)
        
display_data(df)

# Start training if data has been uploaded
if df is not None:
    st.write("The data has been successfully uploaded. You can now import the data to BigQuery and start training.")
    
    # Create a button to import the data to BigQuery and start training
    if st.button("Import data and train"):
        import_new_data_and_train_cached(df)
    

