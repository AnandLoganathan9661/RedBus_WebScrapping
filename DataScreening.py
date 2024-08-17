import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from streamlit_option_menu import option_menu
import json
import re
import base64


def read_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Reading database connection parameters from Configuration file
config = read_config('config.json')

# Define database connection parameters
username = config.get('username')
password = config.get('password')
host= config.get('host')
port= config.get('port')

database = 'Red_Bus'

# Create SQLAlchemy engine
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')

def FetchQueryFromDB(query_string):
    with engine.connect() as connection:
            df = pd.read_sql(query_string,connection)
    return df

def ExeculusiveQuery(query_string):
    with engine.connect() as connection:
            query=text(query_string)
            results=connection.execute(query)
            result=results.fetchone()[0]
    return result


sqlQuery = "select * from bus_routes"
BusRouteDF = FetchQueryFromDB(sqlQuery)  

# Extract unique values for dropdowns
route_name = BusRouteDF["route_name"].unique()
star_rating = BusRouteDF["star_rating"].unique()
max_price = ExeculusiveQuery("Select CEIL(MAX(convert(price,unsigned))/100)*100  as price From bus_routes")
busname = BusRouteDF["busname"].unique()   

#regx pattern to find integer from the text
pattern = r'\d+'

# Initializing a variable
result = None

def filter_function(arg1, arg2, arg3):
    result = None
    selected_columns=f"Busname 'Travels', Bustype 'Type', Departing_time 'Departure', Duration, Reaching_time 'Arrival',Star_Rating 'Rating', Price 'Fare', Seats_Available'Remaining Seats'"
    if arg1 == "Travels":
        searchRequestQuery =f"select {selected_columns} from bus_routes where route_name='{arg2}' and BusName in ({arg3})"
        result= FetchQueryFromDB(searchRequestQuery)
        st.session_state['action'] = FetchQueryFromDB(searchRequestQuery)
    elif arg1 == "Price":
        searchRequestQuery =f"select {selected_columns} from bus_routes where route_name='{arg2}' and Price between 0 and {arg3}"
        result= FetchQueryFromDB(searchRequestQuery)
        st.session_state['action'] = FetchQueryFromDB(searchRequestQuery)
    elif arg1 == "Rating":
        searchRequestQuery =f"select {selected_columns}  from bus_routes where route_name='{arg2}' and star_rating >='{arg3}'"
        result= FetchQueryFromDB(searchRequestQuery)
        st.session_state['action'] = FetchQueryFromDB(searchRequestQuery)
    else:
        #Seats
        searchRequestQuery =f"select {selected_columns}  from bus_routes where route_name='{arg2}' and seats_available>={arg3}"
        result= FetchQueryFromDB(searchRequestQuery)

    # Convert 'Departure & Arrival Time' to string and extract the time part
    result['Departure'] = result['Departure'].astype(str)
    result['Departure'] = result['Departure'].apply(lambda timeValue: str(timeValue).split()[-1])
    result['Arrival'] = result['Arrival'].astype(str)
    result['Arrival'] = result['Arrival'].apply(lambda timeValue: str(timeValue).split()[-1])
    
    return result

# Function to load and encode the image
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: top;
        background-repeat: no-repeat;
        background-attachment: fixed;
        
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the background image (provide the path to your image)
set_background('RedBusTrack_01.png')


with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["About","Data Filter"],
        icons=["info-circle-fill","filter-circle-fill"]
    )

if selected== "About":
    st.subheader("Data Scraping using Selenium Python & Dynamic Filtering using Streamlit App")
    first_paragraph = """
    <b>Problem Statement:</b><br>
    The "Redbus Data Scraping and Filtering with Streamlit Application" aims to revolutionize the transportation industry by providing a comprehensive solution
    for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information
    from Redbus, including bus routes, schedules, prices, and seat availability. By streamlining data collection and providing powerful tools for data-driven
    decision-making, this project can significantly improve operational efficiency and strategic planning in the transportation industry.
    """
    second_paragraph= """
    <b>Approach:</b><br>
    <b>1: Data Scraping:</b><br>
    &nbsp;&nbsp;&nbsp;&nbsp;Use Selenium to automate the extraction of Redbus data including routes, schedules, prices, and seat availability.<br>
    <b>2: Data Storage:</b><br>
    &nbsp;&nbsp;&nbsp;&nbsp;Store the scraped data in a SQL database.<br>
    <b>3: Streamlit Application:</b><br>
    &nbsp;&nbsp;&nbsp;&nbsp;Develop a Streamlit application to display and filter the scraped data.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;Implement various filters such as bustype, route, price range, star rating, availability.<br>
    <b>4: Data Analysis/Filtering using Streamlit:</b><br>
    &nbsp;&nbsp;&nbsp;&nbsp;Use SQL queries to retrieve and filter data based on user inputs.<br>
    &nbsp;&nbsp;&nbsp;&nbsp;Use Streamlit to allow users to interact with and filter the data through the application.<br>
    """
    # Using st.markdown to display the paragraph with Markdown formatting
    st.markdown(f"<p style='text-align:justify;'>{first_paragraph}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:justify;'>{second_paragraph}</p>", unsafe_allow_html=True)

if selected== "Data Filter":
    st.subheader ("Search Bus")
    with st.container():
        col1, col2 = st.columns([1,3])
        with col1:
            selected_filter = option_menu(
                menu_title="Filters",
                options=["Travels","Price","Rating","Seats"],
                icons=["sign-turn-slight-right-fill","tags-fill","star","person-wheelchair"]
            )
        with col2:

            if selected_filter== "Travels":
                route_travels = col2.selectbox("Select the Route", route_name)

                # Fetching Travels name based on route
                query=f"Select distinct busname from Bus_Routes where route_name ='{route_travels}'"
                Busname_DF = FetchQueryFromDB(query)
                bus_name = Busname_DF["busname"].unique() 

                # Create a multiselect widget
                selected_options = st.multiselect(
                    'Choose one or more Travels:',
                    bus_name,  # The list of options derived from ndarray
                )
                # Convert list to a comma-separated string
                temp_selected_options = ', '.join([f"'{item}'" for item in selected_options])

                #Displaying the value what user has selected
                st.write("You have selected : {} Route".format(route_travels))
                st.write("You have selected : ", temp_selected_options)
                
                if st.button('Apply',type="primary"):
                    result = filter_function("Travels",route_travels,temp_selected_options)

            if selected_filter== "Price":
                route_price = col2.selectbox("Select the Route", route_name)
                price_slider = st.slider("Select a ticket fare range", value=100, min_value=0, max_value=int(max_price), step=500)
                temp_price_slider=str(price_slider)

                #Displaying the value what user has selected
                st.write("You have selected : {} Route".format(route_price))
                st.write("Selected Range is:", price_slider)
                
                if st.button('Apply',type="primary"):
                    result = filter_function("Price",route_price,temp_price_slider)

            if selected_filter== "Rating":
                route_rating = col2.selectbox("Select the Route", route_name)
                star_options = ['⭐1 Star & Above', '⭐2 Star & Above', '⭐3 Star & Above', '⭐4 Star & Above', '⭐5 Star']
                selected_stars = st.selectbox('Choose an option:', star_options)
                
                # To get Number value from option i.e Extracting value 1 from '⭐1 Star & Above'
                match = re.search(pattern, selected_stars)
                if match:
                    temp_selected_stars = str(match.group())
                else:
                    temp_selected_stars = None

                #Displaying the value what user has selected
                st.write("You have selected : {} Route".format(route_rating))
                st.write("You have selected : ", temp_selected_stars)

                if st.button('Apply',type="primary"):
                    result = filter_function("Rating",route_rating,temp_selected_stars)

            if selected_filter== "Seats":
                route_seats = col2.selectbox("Select the Route", route_name)
                #Dropdown for choosing number of seat selection
                seats_options = ['1', '2', '3','4','5']
                selected_seat = st.selectbox('Choose number of seats:', seats_options)

                #Displaying the value what user has selected
                st.write("You have selected : {} Route".format(route_seats))
                st.write("You have selected : ", selected_seat)
                
                if st.button('Apply',type="primary"):
                    result = filter_function("Seats",route_seats,selected_seat)
                    
    if result is None:
        st.write(" ")
    elif len(result) == 0:
        st.warning("No data for such criteria, please choose someother.")
    else:
        st.success("Bus details are below")
        st.write(result)
         
    



    
    
    

