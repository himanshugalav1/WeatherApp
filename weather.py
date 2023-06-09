import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
from datetime import datetime,date
import pyowm
from pyowm import OWM
from matplotlib import rcParams
from pytz import timezone
from pyowm.utils import timestamps
import click

#API id from openweathermap
api = '08820823151504804d9d6c720d917d80'
owm = OWM(api)     
mgr = owm.weather_manager()
degree = u'\N{DEGREE SIGN}'

st.title('Weather Forecast ' + "\U0001F600" )
st.write('Write the name of a City and select the Temperature Unit and Graph Type from the sidebar')

city = st.text_input("Name of the City: ", "")

if city == None:
    st.write("Please Enter a city name")

unit = st.selectbox("Select the Temperature Unit: ", ("Celsius", "Fahrenheit"))
graph = st.selectbox("Select the Graph Type: ", ("Line Graph", "Bar Graph"))

b = st.button("SUBMIT")

def pltline(days,mint,maxt):
    days = dates.date2num(days)
    rcParams['figure.figsize']=6,4
    plt.plot(days,maxt,color='green',linewidth = 1,marker='.',markerfacecolor='red',markersize=5) 
    plt.plot(days,mint,color='orange',linewidth = 1,marker='.',markerfacecolor='blue',markersize=5)     
    plt.ylim(min(mint)-3,max(maxt)+4)
    plt.xticks(days)
    #to get current polar axes on fig, If the current axes doesn't exist, or isn't a polar one, the appropriate axes will be created and then returned
    x_y_axis=plt.gca()    
    xaxis_format=dates.DateFormatter('%m/%d')
        
        
    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.legend(["Maximum Temperaure","Minimum Temperature"],loc=1) 
    plt.xlabel('Dates(mm/dd)') 
    plt.ylabel('Temperature') 
    plt.title('5-Day Weather Forecast')   
        
    for i in range(5):
        plt.text(days[i], mint[i]-1.5, mint[i], horizontalalignment='center', verticalalignment='bottom', color='black')
    for i in range(5):
        plt.text(days[i], maxt[i]+0.5, maxt[i], horizontalalignment='center', verticalalignment='bottom', color='black')
    
    st.pyplot()
    plt.clf()

def pltbar(days,mint,maxt):  
        rcParams['figure.figsize']=6,4
        days=dates.date2num(days)
        min_temp_bar=plt.bar(days-0.2, mint, width=0.4, color='y')
        max_temp_bar=plt.bar(days+0.2, maxt, width=0.4, color='r')        
        plt.xticks(days)
        x_y_axis=plt.gca()
        xaxis_format=dates.DateFormatter('%m/%d')
        
        x_y_axis.xaxis.set_major_formatter(xaxis_format)
        plt.xlabel('Dates(mm/dd)') 
        plt.ylabel('Temperature') 
        plt.title('5-Day Weather Forecast')
        
        for bar_chart in [min_temp_bar,max_temp_bar]:
            for index,bar in enumerate(bar_chart):
                height=bar.get_height()
                xpos=bar.get_x()+bar.get_width()/2.0
                ypos=height 
                label_text=str(int(height))
                plt.text(xpos, ypos,label_text,
                        horizontalalignment='center',
                        verticalalignment='bottom',
                        color='black')
        
        
        st.pyplot()
        plt.clf()
        
def find(city,unit,graph):
    mgr=owm.weather_manager()
    days=[]
    dates_2=[]
    mint=[]
    maxt=[]
    forecaster = mgr.forecast_at_place(city, '3h')
    forecast = forecaster.forecast
    if unit=='Celsius':
        units='celsius'
    else:
        units='fahrenheit'
    
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date = day.date()
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
    i=0
    st.write(f"#    Date :  Max - Min  ({unit})")
    for obj in days:
        d=(obj.strftime("%d/%m"))
        st.write(f"### \v {d} :\t  ({maxt[i]} - {mint[i]})")
        i+=1
      
    obs=mgr.weather_at_place(city)
    weather=obs.weather
    st.title(f"Details for {city} currently:")
    st.write(f"### Sky : {weather.detailed_status}")
    st.write(f"### Wind Speed : {weather.wind()['speed']} mph")
    st.write(f"### Sunrise Time : {weather.sunrise_time(timeformat='iso')} GMT")
    st.write(f"### Sunset Time : {weather.sunset_time(timeformat='iso')} GMT")
    
    
    forecaster = mgr.forecast_at_place(city, '3h') 
    st.title("Impending Temperature Changes: ")
    if forecaster.will_have_fog():
        st.write("FOG Alert!")
    if forecaster.will_have_rain():
        st.write("Rain Alert 🌧️")
    if forecaster.will_have_storm():
        st.write("Storm Alert! ⛈️")
    if forecaster.will_have_snow():
        st.write("Snow Alert! ❄️")
    if forecaster.will_have_tornado():
        st.write("Tornado Alert! 🌪️")
    if forecaster.will_have_hurricane():
        st.write("Hurricane Alert! ")
    if forecaster.will_have_clouds():
        st.write("Cloudy Skies ☁️")    
    if forecaster.will_have_clear():
        st.write("Clear Weather! 🪂")
        
if b:
    if not city=="":    
        find(city,unit,graph)

