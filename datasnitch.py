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
from streamlit.components.v1 import html
from streamlit_chat import message
import openai

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

# Add functionality to Ask Baba ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected2 == 'Ask Baba':
    # """This function uses the OpenAI Completion API to generate a 
    # response based on the given prompt. The temperature parameter controls 
    # the randomness of the generated response. A higher temperature will result 
    # in more random responses, while a lower temperature will result in more predictable responses."""
    
    # Set GPT-3 API Key
    openai.api_key = st.secrets['api_secret']
    # Defining a function to generate calls from the API
    def generate_response(prompt):
        completions = openai.Completion.create (
            engine = "text-davinci-003",
            prompt = prompt,
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature = 0.5,
        )
        message = completions.choices[0].text
        return message
    # Set a Title
    st.title("🤖 Ask Baba anything!")
    # Initializing streamlit session statement
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    # Defining function to handle user input
    def get_text():
        input_text = st.text_input("You: ","", key="input")
        return input_text 
    
    # Assigning the function to a variable 
    user_input = get_text()
    
    # Defining a condition to handle the response to the user input 
    if user_input:
        output = generate_response( user_input)
        # adding input and output to a session state
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
    
    # Checking if there is an ouput 
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

     
# Define a line to delimit the footer part ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
st.markdown('---')

# Define Brand Logo image
image = Image.open(r'E:/VS_Code/Webapps/StreamApps/resources/image/techno.png')  

# Add 3 columns with different width
left, middle, right = st.columns([0.3, 0.5, 0.2])
with left:
    #st.write(' ')
    button = """
    <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
    data-name="bmc-button" data-slug="dmcpartnerx" data-color="#FFDD00" data-emoji="🍵"  
    data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" 
    data-coffee-color="#ffffff" ></script>
    """
    html(button, height=70, width=220)
    st.markdown(
        """
        <style>
            iframe[width="150"] {
                position: fixed;
                bottom: 60px;
                left: 40px;
            }
        </style>
        """,
        unsafe_allow_html=True)
with middle:
    st.write(' ')
with right:
    # Add logo to the bottom right position of the page
    st.image(image,  width=150, use_column_width=True)

    