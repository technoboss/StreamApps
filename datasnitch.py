#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
#from io import StringIO
import cv2
from  PIL import Image, ImageEnhance
#import openxl
import time

# Setting the web app basic information
st.set_page_config (page_title="Data|Snitch",
                    page_icon=":game_die:",
                    layout="wide"
)      

# Create two columns with different width
col1, col2 = st.columns([0.2, 0.8])
with col1:                                   # To display brand logo
    st.write(' ')
with col2:                                   # To display the header text using css style
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your file here...</p>', 
                unsafe_allow_html=True)
    
#Add a header and expander in side bar
st.sidebar.markdown('<p class="font">IntelliBiz app</p>', 
                    unsafe_allow_html=True)

with st.sidebar.expander("About our App"):
     st.write("""
        Use this simple app to convert your favorite photo to a pencil sketch, \
        a grayscale image or an image with blurring effect.  \n  \nThis app was \
        created by My Data Talk as a side project to learn Streamlit and computer \
        vision. Hope you enjoy!
     """)
# Add a file uploader to allow users to upload photos
uploaded_file = st.file_uploader("", type=['csv', 'xlsx'])

# Load file to cache using streamlit cache decorator
#@st.cache_data

def datacsv_upload():
        df = pd.read_csv(uploaded_file)
        return df

def dataxl_upload():
        with open(uploaded_file, mode="rb") as excel_file:
            df = pd.read_excel(excel_file) 
        #df = pd.read_excel(uploaded_file, encoding= enc['encoding'])
        return df

# Load the uploaded file
if uploaded_file is not None:
    if uploaded_file.name[0][-4:] == 'xlsx':
        df = dataxl_upload()
        st.dataframe(data=df)
    else:
        df = datacsv_upload()
        st.dataframe(data=df)
        #AgGrid(df)

# Define Brand Logo image
image = Image.open(r'E:/VS_Code/Webapps/StreamApps/resources/images/techno.png')  

# Add a line
st.markdown('---')

# Add 3 columns with different width
left, middle, right = st.columns([0.3, 0.5, 0.2])
with left:
    st.write(' ')
with middle:
    st.write(' ')
with right:
    st.image(image,  width=100, use_column_width=True)