# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from  PIL import Image
from validator_collection import validators
from streamlit_extras.app_logo import add_logo
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
from streamlit_chat import message
import openai
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Setting the web app basic information
st.set_page_config (page_title="Data|weiv",
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

# Adding Brand Logo image on top sidebar
logo = Image.open(r'E:/VS_Code/Webapps/StreamApps/resources/image/techno.png')
st.sidebar.image(logo, width=50, use_column_width=True)

# Add a header and expander in side bar
st.sidebar.markdown('<h1 style="font-size:2.5rem; font-family: Cooper Black; color: #FF9633">Data|weiv</h1>', unsafe_allow_html=True)

# Add a text in an expander frame
with st.sidebar.expander("About our App :rainbow:"):
     st.write("""
        Use this simple app to explore your data in csv or excel file. before \
        using this app you should clean your data first. I you any question \
        just ask Baba. Hey, smile you are on Data|weiv and you will enjoy!
     """)
# ADD A MENU WIDGET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
selected2 = option_menu(None, ["Home", "EDA", "Ask Baba", "Email us"], 
    icons=['house', 'bar-chart-fill', "person-check-fill", "at"], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected2
st.markdown('---')

# ADD FUNCTIONALITY TO ASK BABA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

# ADD FUNCTIONALITY TO EDA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected2 == "EDA":
    # Add title 
    st.title('Get a Quick view in your Data!')
    st.markdown('Here you can upload you data  and visualize it using \
                various plot type. Don\'t forget Baba is your man, you can ask \
                him anything you want to make your work easier.')
    
    # To display a header text using css styling
    st.markdown(""" <style> .font {
    font-size:25px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Please upload a clean data file here...</p>', 
                    unsafe_allow_html=True)
    
    # Defining 2 functions to load csv and excel files
    @st.cache_data
    def datacsv_upload():
            df = pd.read_csv(uploaded_file)
            return df

    def dataxl_upload():
            #with open(uploaded_file, mode="rb") as excel_file:
            df = pd.read_excel(uploaded_file) 
            return df
    
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
            if 'datacsv_upload' in st.session_state:
                df = st.session_state.datacsv_upload
            else:
                df = datacsv_upload()
                st.session_state.datacsv_upload = df
            
        # Defining an horizontal radio button   
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>',
                    unsafe_allow_html=True)
        opt = st.sidebar.radio("Select a graph type:", options=("Bar", "Line", "Scatter"))
    
        # Select columns in your frame
        if opt == 'Bar':
            selected_column = st.sidebar.selectbox('Select a column for the bar plot', df.columns)
            st.write("Histogram Plots")
            fig, ax = plt.subplots(figsize=(10, 4), dpi=200)
            sns.histplot(df[selected_column], color='deepskyblue')
            Plot_title = f'{selected_column} histogram plot'
            ax.set_title(Plot_title , fontweight='bold', color='white', fontsize=15)
            sns.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})
            ax.grid(False)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(axis='both', colors='white')
            sns.despine()
            plt.xticks(rotation = 90)
            st.pyplot(fig)
            #AgGrid(df)

             # Button to download the generated plot
            fn = 'Histogram.png'
            plt.savefig(fn, bbox_inches='tight')
            with open(fn, "rb") as img:
                btn = st.download_button(
                    label="Download Plot",
                    data=img,
                    file_name=fn,
                    mime="image/png"
                )
            # Carrying out some counting on the data
            col1, col2, col3 = st.columns([0.3, 0.6, 0.1])
            with col1:
                st.write('')
            with col2:
                st.write('Some quick statistics')
                grp_bycol = st.sidebar.selectbox('Count', df.columns)
                grp_bycol2 = st.sidebar.selectbox('By', df.columns)
                st.dataframe(df.groupby([grp_bycol]).size().reset_index(name='Count').rename(columns={grp_bycol2:grp_bycol2}))
            with col3:
                st.write(' ')

            # Add data Filter 
            # data = st.sidebar.selectbox('Filter', df.columns)
            # filter = st.sidebar.selectbox('By ', df.columns)
            # st.dataframe()
                         
        if opt == "Line":          
            st.write("Line plot")
            x_axis = st.sidebar.selectbox('Select the x-axis', df.columns)
            y_axis = st.sidebar.selectbox('Select the y-axis', df.columns)
            # Visualize the data with seaborn and matplotlib 
            fig, ax = plt.subplots(figsize=(10, 4), dpi=200)
            sns.lineplot(data=df, x=df[x_axis], y=df[y_axis],
                            marker="o", ax=ax, color='deepskyblue')
            Plot_title = f'{x_axis} and {y_axis} line plot'
            ax.set_title(Plot_title , fontweight='bold', color='white', fontsize=15)
            # Amend figure front and bacground color
            sns.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})
            ax.grid(False)
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(axis='both', colors='white')
            sns.despine()
            plt.xticks(rotation = 90)
            st.pyplot(fig)

            # Button to download the generated plot
            fn = 'line.png'
            plt.savefig(fn, bbox_inches='tight')
            with open(fn, "rb") as img:
                btn = st.download_button(
                    label="Download Plot",
                    data=img,
                    file_name=fn,
                    mime="image/png"
                )

        if opt == "Scatter":
            st.write("Scatter plot")
            x_axis = st.sidebar.selectbox('Select the x-axis', df.columns)
            y_axis = st.sidebar.selectbox('Select the y-axis', df.columns)
            hover_colname = st.sidebar.selectbox('Choose a hover name', df.columns)
            hover_data1 = st.sidebar.selectbox('Choose hover data', df.columns)
            col_color = st.sidebar.selectbox('Choose color column', df.columns)

            # Visualize the data with plotly
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], hover_name=df[hover_colname], 
                             log_x=True, opacity=.8, hover_data=[hover_data1], 
                             color = df[col_color], color_continuous_scale = 'Portland') # "YlGn"

            fig.update_traces(marker=dict(size=15, line=dict(width=1, color='black'), 
                              colorbar=dict(thickness=15), colorscale='Portland'), 
                              marker_coloraxis=None, selector=dict(mode='markers'),
                              showlegend=False)
            
            st.write(fig)
    
# ADD FONCTIONALITY TO EMAIL US ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

    