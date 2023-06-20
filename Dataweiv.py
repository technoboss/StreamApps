# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from  PIL import Image
#from st_aggrid import AgGrid
#from validator_collection import validators
#from streamlit_extras.app_logo import add_logo
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
from streamlit_chat import message
import openai
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plost
import plotly.graph_objects as go
import requests 
from streamlit_lottie import st_lottie

# Setting the web app basic information
st.set_page_config (page_title="Data|weiv",
                    page_icon=":game_die:",
                    layout="wide"
) 
# load the amended css file
with open('style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

img2 = Image.open('Apps_resources/image/techno.png')
st.sidebar.image(img2, width=250)

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
    image = Image.open("Apps_resources/image/dsproject2.png")
    st.image(image, width=1050, use_column_width=True)

# Defining a function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# Assigning image link to a variable
lottie_estate = load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_hbhhy6a8.json')

# ADD A MENU WIDGET ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
selected1 = option_menu(None, ["Home", "EDA", "Dash", "Baba", "Mail"], 
    icons=['house', 'bar-chart-fill', "graph-up-arrow", "person-check-fill", "mailbox"], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected1
st.markdown('---')

# 1. ADD FUNCTIONALITY TO HOME ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected1 == "Home":
    st.title(':red[**_Data|weiv_**] 🐼 a business EDA app')
    # Adding a video file
    video_file = open('Apps_resources/video/dataweiv2.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    # Adding some blank space
    st.sidebar.markdown('##') 
    st.sidebar.markdown('##')  
    st.sidebar.markdown("---")    
    st.sidebar.markdown('##') 
    st.sidebar.markdown('##') 
    st.sidebar.markdown('##') 
    # Adding the animation in the sidebar
    with st.sidebar:
        st_lottie(
                    lottie_estate, 
                    speed=1, 
                    reverse=False, 
                    loop=True, 
                    quality="medium", # medium, high
                    #renderer="svg", # canvas
                    height=None,
                    width=None,
                    key=None )
        st.sidebar.markdown('##') 
        st.sidebar.markdown('''
            ---
            Created with ❤️ by Techno|BOSS.
            ''') 
# 2. ADD FUNCTIONALITY TO EDA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected1 == "EDA":
    # Add title 
    st.title('Get a quick view in your data! :penguin:')
    st.markdown('Here you can upload your data and visualize it using \
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
        opt = st.sidebar.radio("1. Select a graph type:", options=("Bar", "Line", "Scatter"))
    
        # Select columns in your frame
        if opt == 'Bar':
            selected_column = st.sidebar.selectbox('Select a column for the bar plot', df.columns)
            st.write("Histogram Plots")
            fig, ax = plt.subplots(figsize=(10, 4), dpi=200)
            # Amend figure front and bacground color
            #sns.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            # Plotting the data
            sns.histplot(df[selected_column], color='deepskyblue')
            # Defining plot title and configuring its parameters
            Plot_title = f'{selected_column} histogram plot'
            ax.set_title(Plot_title , fontweight='bold', color='white', fontsize=15)    
            ax.grid(False)
            # Defining x and y labels and ticks colors
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(axis='both', colors='white')
            sns.despine()
            # Rotate x label
            plt.xticks(rotation = 90)
            # Display the plot
            st.pyplot(fig)

            # Button to download the generated plot
            filename = 'Histogram.png'
            plt.savefig(filename, bbox_inches='tight')
            with open(filename, "rb") as img:
                btn = st.download_button(
                    label="Download Plot",
                    data=img,
                    file_name=filename,
                    mime="image/png"
                )
            # Carrying out some counting on the data
            st.sidebar.markdown('---')
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>',
                    unsafe_allow_html=True)
            stats = st.sidebar.radio("2. Quick Data Exploration:", options=("Filter by", "Count events"))
            
            if stats == "Filter by":
                filtercol = st.sidebar.selectbox('Display column named ', df.columns)
                filtercol2 = st.sidebar.selectbox('Where row value equal', df[filtercol].unique())
                st.sidebar.markdown('---')
                st.write('Count number events by:')
                st.checkbox("Use container width", value=False, key="use_container_width")
                st.dataframe(pd.DataFrame(df[df[filtercol]==filtercol2].value_counts()), 
                               use_container_width=st.session_state.use_container_width)
                
                # st.dataframe(df.groupby([cnt_bycol]).size().reset_index(name='Count')
                #                 .rename(columns={cnt_bycol1:cnt_bycol1}),
                #                 use_container_width=st.session_state.use_container_width)
                
            elif stats == "Count events":
                cnt_colval = st.sidebar.selectbox('by', df.columns)
                st.sidebar.markdown('---')
                st.write('Count only number of events:')
                st.checkbox("Use container width", value=False, key="use_container_width")
                st.dataframe(df.groupby([cnt_colval]).size(), 
                            use_container_width=st.session_state.use_container_width)
                         
        if opt == "Line":          
            st.write("Line plot")
            x_axis = st.sidebar.selectbox('Select the x-axis', df.columns)
            y_axis = st.sidebar.selectbox('Select the y-axis', df.columns)
            # Set the figure parameters 
            fig, ax = plt.subplots(figsize=(10, 4), dpi=200)
            # Plot the data
            sns.lineplot(data=df, x=df[x_axis], y=df[y_axis],
                            marker="o", ax=ax, color='deepskyblue')
            Plot_title = f'{x_axis} and {y_axis} line plot'
            ax.set_title(Plot_title , fontweight='bold', color='white', fontsize=15)
            # Amend figure front and bacground color
            #sns.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            # disabble background grid
            ax.grid(False)
            # Set x an y labels and ticks color 
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(axis='both', colors='white')
            sns.despine()
            # rotate x label
            plt.xticks(rotation = 90)
            st.pyplot(fig)

            # Button to download the generated plot
            filename = 'line.png'
            plt.savefig(filename, bbox_inches='tight')
            with open(filename, "rb") as img:
                btn = st.download_button(
                    label="Download Plot",
                    data=img,
                    file_name=filename,
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
# 3. ADD FUNCTIONALITY TO DASH ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected1 == "Dash": 
    # ~~~~~~~~~~~~~~~~~~~~~TAKING CARE OF THE SIDEBAR ~~~~~~~~~~~~~~~~~~~~~~~
    # To display a header text using css styling
    st.markdown(""" <style> .font {
    font-size:20px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Please upload a clean data file here...</p>', 
                    unsafe_allow_html=True) 
    
    # Add a file uploader to allow users to upload photos
    uploaded_file2 = st.file_uploader("", type=['csv', 'xlsx'])
    
     # Add title 
    st.title('Get a Dashbord view! :chart:')
    st.markdown('Use this app to displays some KPIs and various visualization types from your data.\
                Our app will only the first 100 rows of your files. :red[**_ONLY USE NUMERICAL DATA TO VIEW METRICS._**]')
    st.markdown('---')
    # Defining 2 functions to load csv and excel files
    @st.cache_data
    def datacsv_upload2():
            df = pd.read_csv(uploaded_file2)
            return df

    def dataxl_upload2():
            df = pd.read_excel(uploaded_file2.name) 
            return df
    
    # Load the uploaded file
    if uploaded_file2 is not None:
        if uploaded_file2.name[0][-4:] == 'xlsx':
            df = dataxl_upload2()
            #st.dataframe(data=df)
        else:
            df = datacsv_upload2()
            #st.dataframe(data=df)
            if 'datacsv_upload2' in st.session_state:
                df = st.session_state.datacsv_upload2
            else:
                df = datacsv_upload2()
                st.session_state.datacsv_upload2 = df 

        st.sidebar.header('Dashboard Builder')
        
        # Defining 3 column to laverage the streamlit metric feature
        st.sidebar.markdown('---')
        st.markdown('### KPI Metrics')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.sidebar.subheader('Select KPI Metrics')
            filtercol = st.sidebar.selectbox('Select a :red[**numerical**] column to see Metrics', df.columns)
            
            # Defining stats data frame
            sum_df = df[filtercol].sum()
            mean_df = df[filtercol].mean()
            range_df = (df[filtercol].max() - df[filtercol].min())
            min_df = df[filtercol].min() 
            max_df = df[filtercol].max()
            count_df = df[filtercol].count()
            med_df = df[filtercol].median()
            std_df = df[filtercol].std()    

            st.metric(
                label=f"SUM {filtercol}", 
                value= f"{sum_df:.2f}", 
                delta=f"STD: {std_df:.0f}")
        with col2:
            st.metric(
                label=f"AVG. {filtercol}", 
                value=f"{mean_df:.2f}", 
                delta=f"MAX: {max_df:.0f}")
        with col3:
            st.metric(
                label=f"Event COUNT", 
                value=f"{count_df:.2f}", 
                delta=f"RANGE: {range_df:.0f}")
        st.markdown('---')      
        # Row B
        # Using 2 columns to display a heatmap and donut plot
        c1, c2 = st.columns((8,2))
        with c1:
            st.markdown('### Bar plot')
            st.sidebar.markdown('---')
            st.sidebar.subheader(':red[**Bar plot parameter**]')
            # Sidebar filter
            #Groupby_df = st.sidebar.selectbox('Select a column df', df.columns)
            # defining a pandas groupy Dataframe
            #heat_df = df.groupby([Groupby_df]).value_counts().unstack().fillna(0)
            x_axis = st.sidebar.selectbox('Select the x-axis', df.columns)
            y_axis = st.sidebar.selectbox('Select the y-axis', df.columns)
            color = st.sidebar.selectbox('Select color param', df.columns)
            #data_df = st.sidebar.selectbox('Select date param', df.columns)

            fig = px.bar(df, x=x_axis, y=y_axis, color=color)
            #fig.update_layout(width=500,height=500)

            # Size the figure
            #fig, ax = plt.subplots(figsize=(12, 5), dpi=160)
            # set the figure facecolor opacity
            #fig.patch.set_alpha(0.0)
            # plot the correlation heatmap
            #sns.heatmap(data= heat_df.corr(), linewidth=.1, fmt='.2f',
                        #cmap='RdBu', annot=True)
            #sns.heatmap(data=heat_df, cmap=sns.color_palette("crest", as_cmap=True))
            
            # define x an y axis label color
            #ax.xaxis.label.set_color('white')
            #ax.yaxis.label.set_color('white')
            #ax.tick_params(axis='both', colors='white', labelsize=12) 
            # display the plot
            st.write(fig, use_container_width=True)

        with c2:
            st.markdown('### Donut chart')
            st.sidebar.markdown('---')
            st.sidebar.subheader(':red[**Donut chart parameter**]')
            # setting up the filters
            donut_filter1 = st.sidebar.selectbox('Select column for color', df.columns)
            donut_filter2 = st.sidebar.selectbox('Select :red[**numerical**] data', df.columns)
            donut_filter5 = st.sidebar.selectbox('Select thetha', df.columns)
            donut_data = df.nlargest(3, donut_filter2)

            plost.donut_chart(
                    data=donut_data,
                    theta = donut_filter5,
                    color=donut_filter1,
                    legend='bottom',
                    use_container_width=True)
        # Row C
        st.sidebar.markdown('---')
        st.sidebar.subheader(':red[**Line chart parameters**]')
        x_axis1 = st.sidebar.selectbox('Select your x axis', df.columns)
        y_axis2 = st.sidebar.selectbox('Select your y axis', df.columns)
        plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)
        st.markdown('### Line chart')
        st.line_chart(df, x =  x_axis1, y = y_axis2, height = plot_height)
            
# 4. ADD FUNCTIONALITY TO ASK BABA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected1 == 'Baba':
    # """This function uses the OpenAI Completion API to generate a 
    #    response based on the given prompt. """
    
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
    
# 5. ADD FONCTIONALITY TO EMAIL US ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if selected1 == 'Mail':
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
image = Image.open('Apps_resources/image/techno.png')  

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

# Developped by Don Curtis