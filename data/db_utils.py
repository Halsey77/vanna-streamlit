from vanna.remote import VannaDefault
import sqlite3 as db
import pandas as pd
import streamlit as st

# DATABASE FUNCTIONS----------------------------------------------------------


@st.cache_resource(ttl=3600)
def connect_db():
    conn = db.connect(st.secrets.get("SQLITE_DB"), check_same_thread=False)
    return conn


CREATE_TABLES_SQL = """
    CREATE TABLE IF NOT EXISTS HANOI_AIR (
        date TEXT PRIMARY KEY,
        pm25 REAL,
        pm10 REAL,
        o3 REAL,
        no2 REAL,
        so2 REAL,
        co REAL,
        temp REAL,
        dewp REAL,
        visib REAL,
        fog INTEGER,
        AQI REAL
    )
"""


@st.cache_resource(ttl=3600)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLES_SQL)
    conn.commit()


@st.cache_resource(ttl=3600)
def add_init_data():
    conn = connect_db()
    df = pd.read_csv("data/hanoi_info.csv")
    df.to_sql("HANOI_AIR", conn, if_exists="replace", index=False)


@st.cache_resource(ttl=3600)
def init_db():
    create_table()
    add_init_data()


def add_new_data(df: pd.DataFrame):
    conn = connect_db()
    cur = conn.cursor()
    
    # get all table names
    name_cur = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    # drop all table currently in the db
    for name in name_cur:
        cur.execute("DROP TABLE IF EXISTS " + name[0])

    # add new table
    df.to_sql("AIR", conn, if_exists="replace", index=False)

    return "AIR"
