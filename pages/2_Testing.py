# TODO: Remove this file after testing is complete.
import streamlit as st
from data.db_utils import init_db
from vanna_calls import get_all_tables, get_all_tables_and_data, drop_table

st.markdown("# Testing")

init_db()

# tables = get_all_tables()
tables, tables_data = get_all_tables_and_data()

st.write("Current tables in the database:")
st.write(tables)

st.write("All tables in the database and their data:")
for table, data in tables_data.items():
    st.write(f"Table: {table}")
    st.write(data)
    st.write("")