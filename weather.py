import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime
from pyowm import OWM
from matplotlib import rcParams

#API id from openweathermap
api = 'b6fc092cc0b23af60741998d06732f01'
owm = OWM(api)     
mgr = owm.weather_manager()
degree = u'\N{DEGREE SIGN}'

st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("<h1 style='text-align: center; '>WEATHER FORECAST \U0001F326 </h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; '>Write the name of a City and select the Temperature Unit and Graph Type from below</h6>", unsafe_allow_html=True)

st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
city = st.text_input("Name of the City: ", "")
st.text(" ")
unit = st.selectbox("Select the Temperature Unit: ", ("Celsius", "Fahrenheit"))
st.text(" ")
graph = st.selectbox("Select the Graph Type: ", ("Line Graph", "Bar Graph"))
st.text(" ")
btn = st.button("SUBMIT")

# function to plot the line curve
def pltline(days, mint, maxt):
    days = dates.date2num(days)
    rcParams['figure.figsize']=6,4
    plt.plot(days,maxt,color='#FF2E2E', linewidth = 1, marker='.', markerfacecolor='red', markersize=7 ) 
    plt.plot(days,mint,color='#00B7EB', linewidth = 1, marker='.', markerfacecolor='blue', markersize=7 )     
    plt.ylim(min(mint)-3,max(maxt)+4)
    plt.xticks(days)
    #to get current polar axes on fig, If the current axes doesn't exist, or isn't a polar one, the appropriate axes will be created and then returned
    x_y_axis=plt.gca()
    xaxis_format=dates.DateFormatter('%d/%m')


    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.legend(["Maximum Temperaure","Minimum Temperature"],loc=1) 
    plt.xlabel('Dates (dd/mm)')
    plt.ylabel('Temperature')
    plt.title('5-Day Weather Forecast')
        
    for i in range(6):
        plt.text(days[i], mint[i]-1.5, mint[i], horizontalalignment='center', verticalalignment='bottom', color='black')
    for i in range(6):
        plt.text(days[i], maxt[i]+0.5, maxt[i], horizontalalignment='center', verticalalignment='bottom', color='black')
    
    st.pyplot()
    plt.clf()

# Function to plot the bar curve
def pltbar(days,mint,maxt):  
        rcParams['figure.figsize']=6,4
        days=dates.date2num(days)
        min_temp_bar=plt.bar(days-0.17, mint, width=0.3, color='#00B7EB')   # congfiguring the min bar
        max_temp_bar=plt.bar(days+0.17, maxt, width=0.3, color='#FF2E2E')   # configuring the max bar
        plt.xticks(days)
        x_y_axis=plt.gca()
        xaxis_format=dates.DateFormatter('%d/%m')
        
        x_y_axis.xaxis.set_major_formatter(xaxis_format)
        plt.xlabel('Dates (dd/mm)')
        plt.ylabel('Temperature')
        plt.title('5-Day Weather Forecast')
        
        for bar_chart in [min_temp_bar, max_temp_bar]:
            for index,bar in enumerate(bar_chart):
                height=bar.get_height() # height of the bar
                xpos=bar.get_x()+bar.get_width()/2.0    # x position of temperature text above the bar
                ypos=height-0.4
                label_text=str(int(height)) # text of temperature value
                plt.text(xpos, ypos, label_text, horizontalalignment='center', verticalalignment='bottom', color='black')
        
        st.pyplot()
        plt.clf()
        
# Function to find the city and show us the page as per the details entered
def find(city,unit,graph):
    mgr=owm.weather_manager()
    days=[] # total days you want to print the data for
    dates_2=[]
    mint=[] # minimum temperature
    maxt=[] # maximum temperature
    # forcaster stores the data of forecast of the entered city
    forecaster = mgr.forecast_at_place(city, '3h')
    forecast = forecaster.forecast
    # set the units as per user input
    if unit=='Celsius':
        units='celsius'
    else:
        units='fahrenheit'
    
    # 
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())   # get the current day 
        date = day.date()   # current date
        if date not in dates_2:
            dates_2.append(date)
            mint.append(None)
            maxt.append(None)
            days.append(date)
        temperature = weather.temperature(units)['temp']
        
        if not mint[-1] or temperature < mint[-1]:
            mint[-1]=temperature
        if not maxt[-1] or temperature > maxt[-1]:
            maxt[-1]=temperature
    
    if graph=="Line Graph":
        pltline(days,mint,maxt)
    elif graph=="Bar Graph":
        pltbar(days,mint,maxt)
    
    st.text(" ")
    # printing weather of current day and next 5 days
    i=0
    st.write(f"#    Date :  Max - Min  ({unit})")
    for obj in days:
        d=(obj.strftime("%d/%m"))
        st.write(f" #### • {d} :\t  ( {maxt[i]} - {mint[i]} )")
        i+=1
    
    st.text(" ")
    # showing detailed data 
    obs=mgr.weather_at_place(city) # getting the weather details of the given city
    weather=obs.weather # retrieve weather object
    st.title(f"Details for {city} currently:")  
    st.write(f"#### • Sky : {weather.detailed_status}")    # getting the detailed weather status
    st.write(f"#### • Wind Speed : {weather.wind()['speed']} mph")     # getting the wind speed 
    st.write(f"#### • Sunrise Time : {weather.sunrise_time(timeformat='iso')} GMT")    # getting sunrise time
    st.write(f"#### • Sunset Time : {weather.sunset_time(timeformat='iso')} GMT")      # getting sunset time
    
    # showing any imepending temperature changes or alerts
    forecaster = mgr.forecast_at_place(city, '3h') 
    st.title("Impending Temperature Changes: ")
    if forecaster.will_have_fog():
        st.write("##### • FOG Alert!")
    if forecaster.will_have_rain():
        st.write("##### • Rain Alert 🌧️")
    if forecaster.will_have_storm():
        st.write("##### • Storm Alert! ⛈️")
    if forecaster.will_have_snow():
        st.write("##### • Snow Alert! ❄️")
    if forecaster.will_have_tornado():
        st.write("##### • Tornado Alert! 🌪️")
    if forecaster.will_have_hurricane():
        st.write("##### • Hurricane Alert! ")
    if forecaster.will_have_clouds():
        st.write("##### • Cloudy Skies ☁️")    
    if forecaster.will_have_clear():
        st.write("##### • Clear Weather! 🪂")
        
if btn:
    if city == "":
        st.warning('Please enter the city name you want to search for !', icon="⚠️")
    if not city=="":    
        find(city,unit,graph)

