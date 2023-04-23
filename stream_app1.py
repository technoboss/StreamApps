# Import necessary Python libraries
import pandas as pd
import folium
import geopandas as gpd
import json
from folium.features import GeoJsonPopup, GeoJsonTooltip
import streamlit as st
from streamlit_folium import folium_static
from streamlit_lottie import st_lottie
import requests 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
sns.set()

# Setting the web app basic information
st.set_page_config (page_title="US Housing market",
                    page_icon=":house:",
                    layout="wide"
)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA PREPARATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Load file to cache using streamlit cache decorator
@st.cache_data
# Define a function to load the data 
def read_csv(path):
    return pd.read_csv(path, compression='gzip', sep='\t', quotechar='"')

# Retrieve relevent field in our dataset
housing_price_df=read_csv('E:/VS_Code/Webapps/StreamApps/resources/state_market_tracker.tsv000.gz')
housing_price_df=housing_price_df[['period_begin','period_end','period_duration','property_type','median_sale_price','median_sale_price_yoy','homes_sold','state_code']]
housing_price_df=housing_price_df[(housing_price_df['period_begin']>='2020-10-01') & (housing_price_df['period_begin']<='2021-10-01')]

# Display the dataframe in the app
#st.write(housing_price_df)  

# Define a function to load a geo pandas file
@st.cache_data
def read_file(path):
    return gpd.read_file(path)

# Read the geojson file
gdf = read_file('E:/VS_Code/Webapps/StreamApps/resources/us-state-boundaries.geojson')

# Display the dataframe in the app
#st.write(gdf.head())

# Merge the housing market data and the geojson file into one dataframe
df_final = gdf.merge(housing_price_df, left_on="stusab", right_on="state_code", how="outer")
df_final=df_final[['period_begin','period_end','period_duration','property_type','median_sale_price','median_sale_price_yoy','homes_sold','state_code','name','stusab','geometry']]
df_final= df_final[~df_final['period_begin'].isna()]

# Write the final df on the web app
#st.write(df_final.head()) 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~BUILDING THE WEB APP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add title and subtitle to the main interface
st.title("U.S. Real Estate Insights")
st.markdown("Where are the trendiest housing markets in the US? Select a metrics you are interested in to get answer. Hover over the map to view more details.")

# Create three columns/filters
col1, col2, col3 = st.columns(3)

with col1:
     period_list=df_final["period_begin"].unique().tolist()
     period_list.sort(reverse=True)
     year_month = st.selectbox("Snapshot Month", period_list, index=0)

with col2:
     prop_type = st.selectbox(
                "View by Property Type", ['All Residential', 'Single Family Residential', 'Townhouse','Condo/Co-op','Single Units Only','Multi-Family (2-4 Unit)'] , index=0)

with col3:
     metrics = st.selectbox("Select Housing Metrics", ["median_sale_price","median_sale_price_yoy", "homes_sold"], index=0)

# Update the data frame accordingly based on user input
#df_final=df_final.dropna()
df_final=df_final[df_final["period_begin"]==year_month]
df_final=df_final[df_final["property_type"]==prop_type]
df_final=df_final[['period_begin','period_end','period_duration','property_type','median_sale_price_yoy',metrics,"homes_sold",'state_code','name','stusab','geometry']]

#st.write(df_final)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ADD THE CHOROPLETH MAP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Initiate a folium map
m = folium.Map(location=[40, -100], zoom_start=4,tiles=None)
folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m)

#Plot Choropleth map using folium
choropleth1 = folium.Choropleth(
    geo_data=gdf,                                   # Geojson file for the Unite States
    name='Choropleth Map of U.S. Housing Prices',
    data=df_final,                                  # Dataframe created in the data preparation step
    columns=['state_code', metrics],                # 'state code' and 'metrics' are the two columns in the dataframe used to grab the median sales price for each state and plot it in the choropleth map
    key_on='feature.properties.stusab',             # Geojson file key use to grab the geometries for each state in order to add the geographical boundary layers to the map
    fill_color='viridis',  #'YlGn'
    nan_fill_color="White",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Housing Market Metrics',
    highlight=True,
    line_color='black').geojson.add_to(m)

# Add tooltips to the map
geojson1 = folium.features.GeoJson(
               data=df_final,
               name='United States Housing Prices',
               smooth_factor=2,
               style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
               tooltip=folium.features.GeoJsonTooltip(
                   fields=['period_begin',
                           'period_end',
                           'name',
                           metrics,],
                   aliases=["Period Begin:",
                            'Period End:',
                            'State:',
                            metrics+":"], 
                   localize=True,
                   sticky=False,
                   labels=True,
                   style="""
                       background-color: #F0EFEF;
                       border: 2px solid black;
                       border-radius: 3px;
                       box-shadow: 3px;
                   """,
                   max_width=800,),
                    highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                   ).add_to(m) 

folium_static(m)

st.write('Thanks to Matt Chapman for his insight tutorial')
st.markdown("---")

# Create a sidebar 
st.sidebar.markdown("### US Real Estate Market.")
st.sidebar.markdown("Get an insight into the US Real Estate market. Choose how you would like to visualize it.")
opt = st.sidebar.radio("Select a graph type", options=("Line", "Scatter", "Bar"))
if opt == "Line":
    # Visualize the data with seaborn and matplotlib 
    fig, ax = plt.subplots(figsize=(10, 5), dpi=160)
    sns.lineplot(data=df_final, y=df_final['median_sale_price'], x=df_final['homes_sold'],
                 marker="o", ax=ax, color='deepskyblue')
    ax.set_title('MEDIAN PRICE AND NUMBER OF HOMES SOLD PER STATE', fontsize=13,
                fontweight='bold')
    ax.set_ylabel('Median sale price')
    ax.set_xlabel('Homes sold')
    plt.show()
    st.write(fig)
if opt == "Scatter":
    # Visualize the data with plotly
    fig = px.scatter(df_final, x=df_final['median_sale_price'], y=df_final['homes_sold'],
                hover_name=df_final['name'], log_x=True, opacity=.8, 
                color=df_final['median_sale_price_yoy'],
                hover_data=["period_begin","period_end","median_sale_price",
                            "median_sale_price", "homes_sold"],
                labels={
                     "median_sale_price": "Median sale price",
                     "homes_sold": "Number of homes sold",
                     "median_sale_price_yoy": "Year-over-Year change"
                }, color_continuous_scale = "YlGn"
    )
    fig.update_traces(marker=dict(size=15, line=dict(width=1.5, color='black')),marker_coloraxis=None, 
                  selector=dict(mode='markers'))

    fig.update_layout(title = '<b>MEDIAN PRICE AND NUMBER OF HOMES SOLD PER STATE</b>', title_x=0.2)
    #coloraxis_colorbar_x=1.2 # colobar position
    st.write(fig)
if opt == 'Bar':
    # Visualize the data with seaborn and matplotlib 
    fig, ax = plt.subplots(figsize=(10, 5), dpi=160)
    sns.histplot(data=df_final, x='homes_sold', color='deepskyblue')
    ax.set_title('FREQUENCY OF MEDIAN PRICE HOMES SOLD PER STATE', fontsize=13,
                fontweight='bold')
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Median sale price')
    plt.show()
    st.write(fig)

# Defining 2 function to load Lottie animation
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Loading the animations
lottie_file = load_lottiefile('E:/VS_Code/Webapps/StreamApps/resources/graph-animation-12.json')
lottie_estate = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_leneywe2.json')

# Adding the animation in the sidebar
with st.sidebar:
    st_lottie(
                lottie_estate, 
                speed=1, 
                reverse=False, 
                loop=True, 
                quality="low", # medium, high
                #renderer="svg", # canvas
                height=None,
                width=None,
                key=None )
#st_lottie(lottie_file, key="hello")

st.markdown("---")

# Adding a frame of 3 columns
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Designed by:')
with col2:
    image = Image.open('E:/VS_Code/Webapps/StreamApps/resources/techno.png')
    st.image(image, width=250)
with col3:
    #st.write(' ')
    st_lottie(lottie_file, 
            key="hello",
            height=100,  
            width=250,
            speed=1,
            loop=True,
            reverse=False,
            quality='medium')
