import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import datetime

GEOPHONE_DATA_PATH = "./data/"
FILES_HEADER = ["Timestamp", "Geophone_1", "Geophone_2", "Geophone_3", "Geophone_4", "Geophone_5", "Geophone_6"]
TIME_RANGE_LIST = [i/(12000/6) for i in range(1,12001)]
ACQUISITION_START_DATE = datetime.date(2015,3,5)
ACQUISITION_END_DATE = datetime.date(2024,7,15)

# ========== PAGE SETUP ==========
st.set_page_config(
    page_title="Geophone data visualization",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title('Visualization of measurements from July 15, 2024')



# ========== FUNCTIONS DEFINITION ==========
@st.cache_data
def get_geophone_data(path):
    df = pd.read_csv(path, skiprows=[1], usecols=FILES_HEADER, index_col=0)
    return df

@st.cache_data
def get_csv_file_list(path):
    file_list = os.listdir(path)
    return file_list

def date_range_input_behavior():
    pass

# ========== SESSION STATE ==========
if 'date_range' not in st.session_state:
    st.session_state.date_range = (ACQUISITION_END_DATE, ACQUISITION_END_DATE)


# ========== SIDE BAR ==========
files = get_csv_file_list(GEOPHONE_DATA_PATH)

if 'selected_file' not in st.session_state:
    st.session_state.selected_file = files[0]

with st.sidebar:
    select_file = st.selectbox('Select a file', files)
    
    my_date_input = st.date_input(
        "Select range of data acquisition",
        value=st.session_state.date_range,
        min_value=ACQUISITION_START_DATE,
        max_value=ACQUISITION_END_DATE
    )
    
    if st.button('Update'):
        st.session_state.selected_file = select_file
        st.session_state.date_range = my_date_input
        


# ========== FILE HANDLING ==========
current_file_path = GEOPHONE_DATA_PATH + st.session_state.selected_file
st.write(st.session_state.selected_file)
geophone_df = get_geophone_data(current_file_path)



# ========== MAIN PAGE ==========
with st.container():
    fig = px.line(
        data_frame=geophone_df,
        x=TIME_RANGE_LIST,
        y=FILES_HEADER[1:],
    )
    
    fig.update_xaxes(nticks=40)
    
    fig.update_layout(
        title="Geophone measurements",
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        legend_title="Geophone",
    )
    
    st.plotly_chart(fig, use_container_width=True)


with st.container():
    st.subheader('Raw data')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write(geophone_df)
    with col2:
        st.write(geophone_df.describe())



    
