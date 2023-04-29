#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from  PIL import Image
#from openpyxl import load_workbook
from validator_collection import validators
from streamlit_extras.app_logo import add_logo
from streamlit_option_menu import option_menu

# Setting the web app basic information
st.set_page_config (page_title="Data|Snitch",
                    page_icon=":game_die:",
                    layout="wide"
) 

# Adjusting page Top and bottom padding
st.markdown("""
            <style>
                    .block-container {
                        padding-top:0rem;
                        padding-bottom: 0rem
                    }
            </style>
            """, unsafe_allow_html=True)

# Adding top header image into a container
with st.container():
    image = Image.open("E:/VS_Code/Webapps/StreamApps/resources/image/dsproject2.png")
    st.image(image, width=1050, use_column_width=True)

# Add logo to sidebar
#@extra
def add_logo(logo_url: str):
    validators.url(logo_url) 
    st.markdown(
        f"""
       <style>
            [data-testid="stSidebarNav"] {{
                background-image: url({logo_url});
                background-repeat: no-repeat;
                padding-top: 80px;;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True)

with st.sidebar:
     add_logo("https://raw.githubusercontent.com/technoboss/StreamApps/main/resources/images/techno.png")

# Defining 2 functions to load csv and excel files
#@st.cache_data
def datacsv_upload():
        df = pd.read_csv(uploaded_file)
        return df

def dataxl_upload():
        #with open(uploaded_file, mode="rb") as excel_file:
        df = pd.read_excel(uploaded_file) 
        return df

# Add a header and expander in side bar
st.sidebar.markdown('<h1 style="font-size:2.5rem; font-family: Cooper Black; color: #FF9633">Data|Snitch</h1>', unsafe_allow_html=True)

# Add a text in an expander frame
with st.sidebar.expander("About our App :rainbow:"):
     st.write("""
        Use this simple app to convert your favorite photo to a pencil sketch, \
        a grayscale image or an image with blurring effect.  \n  \nThis app was \
        created by My Data Talk as a side project to learn Streamlit and computer \
        vision. Hope you enjoy!
     """)
# Add a menu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
selected2 = option_menu(None, ["Home", "EDA", "Ask Baba", "Email us"], 
    icons=['house', 'bar-chart-fill', "person-check-fill", "at"], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected2
st.markdown('---')

# Add functionality to EDA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected2 == "EDA":
    # To display a header text using css styling
    st.markdown(""" <style> .font {
    font-size:30px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your file here...</p>', 
                    unsafe_allow_html=True)
    
    # Add a file uploader to allow users to upload photos
    uploaded_file = st.file_uploader("", type=['csv', 'xlsx'])

    # Load the uploaded file
    if uploaded_file is not None:
        if uploaded_file.name[0][-4:] == 'xlsx':
            df = dataxl_upload()
            st.dataframe(data=df)
        else:
            df = datacsv_upload()
            st.dataframe(data=df)
            #AgGrid(df)

# Add Functionality to Email us ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected2 == 'Email us':
    st.header(':globe_with_meridians: Get in touch with us!')
    contact_form = """
    <form action="https://formsubmit.co/m.curtisdon@yahoo.co.uk" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Type your message"></textarea>
        <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

    # Use local CSS code 
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Calling the function
    local_css("style/style.css")
     
# Define a line to delimit the footer part ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
st.markdown('---')

# Define Brand Logo image
image = Image.open(r'E:/VS_Code/Webapps/StreamApps/resources/image/techno.png')  

# Add 3 columns with different width
left, middle, right = st.columns([0.3, 0.5, 0.2])
with left:
    st.write(' ')
with middle:
    st.write(' ')
with right:
    # Add logo to the bottom right position of the page
    st.image(image,  width=100, use_column_width=True)