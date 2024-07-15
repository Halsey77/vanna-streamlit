import streamlit as st
import numpy as np
import pandas as pd

from vanna_calls import import_new_data_and_train_cached

st.set_page_config(page_title="Input data", layout="wide")

# Set up main page
st.markdown("# Input data")
st.write(
    "Thêm dữ liệu mới vào hệ thống và huấn luyện mô hình dự đoán chất lượng không khí."
)


# Choose location
def choose_location_selection(options):
    location = st.selectbox("Chọn địa điểm", options)
    return location


options_dict = {"Hà Nội": "HANOI_AIR", "Hồ Chí Minh": "HCM_AIR"}
options = list(options_dict.keys())
location_name = choose_location_selection(options)
location_db_name = options_dict[location_name]


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
    st.write("Dữ liệu đã tải lên:")
    if df is not None:
        st.write(df)

if df is not None:
    display_data(df)

# Start training if data has been uploaded and location has been selected
if location_name is not None and df is not None:
    st.write(
        f"Dữ liệu đã tải lên và địa điểm {location_name} đã chọn. Bấm vào nút bên dưới để tiếp tục."
    )

    # Create a button to import the data to BigQuery and start training
    if st.button("Nhập dữ liệu và bắt đầu huấn luyện"):
        import_new_data_and_train_cached(df, location_db_name)
        
