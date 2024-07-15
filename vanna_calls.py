import streamlit as st
from vanna.remote import VannaDefault
import pandas as pd

from data.db_utils import add_new_data


@st.cache_resource(ttl=3600)
def setup_vanna():
    vn = VannaDefault(api_key=st.secrets.get("VANNA_API_KEY"), model="chinook")
    vn.connect_to_sqlite(st.secrets.get("SQLITE_DB"))
    return vn


@st.cache_data(show_spinner="Generating sample quest    ions ...")
def generate_questions_cached():
    vn = setup_vanna()
    return vn.generate_questions()


@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)


@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)


@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str):
    vn = setup_vanna()
    return vn.run_sql(sql=sql)


@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)


@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code


@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)


@st.cache_data(show_spinner="Generating followup questions ...")
def generate_followup_cached(question, sql, df):
    vn = setup_vanna()
    return vn.generate_followup_questions(question=question, sql=sql, df=df)


@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(question, df):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)


def train_model_with_table(table_name):
    vn = setup_vanna()
    df_schema = vn.run_sql(f"SELECT * FROM {table_name}")
    plan = vn.get_training_plan_generic(df_schema=df_schema)
    vn.train(plan=plan)

    return plan


@st.cache_data(show_spinner="Importing new data and training ...")
def import_new_data_and_train_cached(df):
    table_name = add_new_data(df)
    return train_model_with_table(table_name)


# TODO: REMOVE THESE FUNCTIONS AFTER TESTING IS COMPLETE
# TESTING FUNCTIONS------------------------------------------------------------


def get_all_tables():
    vn = setup_vanna()
    return vn.run_sql("""SELECT name FROM sqlite_master WHERE type='table';""")


def get_all_tables_and_data():
    vn = setup_vanna()
    tables = get_all_tables().to_numpy()
    table_data = {}
    for table in tables:
        table_name = table[0]
        table_data[table_name] = vn.run_sql(f"SELECT * FROM {table_name};")
    return tables, table_data


def get_table_data(table_name):
    vn = setup_vanna()
    return vn.run_sql(f"SELECT * FROM {table_name};")


def drop_table(table_name):
    vn = setup_vanna()
    vn.run_sql(f"DROP TABLE {table_name};")
