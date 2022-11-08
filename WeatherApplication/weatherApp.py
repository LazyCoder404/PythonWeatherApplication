#******************************************************
#Created by: Venkata Murali Krishna Gedela, C0839164  *
#-----------------------------------------------------*
#A simplified weather application which displays the  *
# current weather information for a given city        *
#-----------------------------------------------------*
#open weather API Key                                 *
#97a5f78c0717ab39f49e78f14859d511                     *
#******************************************************
from cgitb import text
from distutils.command.config import LANG_EXT
import time
from tkinter import messagebox
import pyowm
from tkinter import *
import tkinter as tk

#API key for requesting the data
OPEN_WEATHER_API_KEY = "97a5f78c0717ab39f49e78f14859d511"
cityw = ""
#Create the base GUI window
root = Tk()
root.title("Weather Application")#Application name
root.geometry("600x400+300+200")#Dimensions and position of the GUI
root.resizable(False, False)#disable minimize and maximize options
root.configure(bg="#B8FFF9")#set the background color



"""
Function get_weather()
gets all the weather information for the @param city
and updates the respective GUI elements
"""
def get_weather(city="Sarnia,Canada"):
    #create the OWM object using the api key
    owm = pyowm.OWM(OPEN_WEATHER_API_KEY)
    mgr = owm.weather_manager()
    try:
        #get the city name entered in the search box
        city = text_field_city.get()
        if(city == ""):
            city="Sarnia,Canada"
        else:
            city = city.capitalize()#set the first letter of the city name to Upper case
        cityw = city
        #get the weather info
        observation = mgr.weather_at_place(city)
        #Alias the weather object
        w = observation.weather
        #temperature information in celsius
        tempInCelcius = w.temperature('celsius')
        #temperature information in Fahrenheit
        tempInFahrenheit = w.temperature('fahrenheit')
        
        #Format the current tempe to display in celsius and fahrenheit example: 0°C | 32°F
        current_temp = str(round(tempInCelcius['temp'])) + '°C' + ' | ' + str(round(tempInFahrenheit['temp'])) + '°F' 
        #Get the weather description
        status = w.detailed_status
        #Get the wind information
        wind = str(w.wind()['speed']) + " km/h"
        #Get the humidity in the air
        humidity = str(w.humidity) + "%"

        #update the GUI elements
        lable_city.config(text=city)
        lable_current_temp.config(text=current_temp)
        lable_status.config(text=status)
        lable_wind_value.config(text=wind)
        lable_Humidity_value.config(text=humidity)
        
        #Reset the timer when new data is calculated
        refresh_timer()

    except Exception as e:
        #messagebox.showerror("Weather Application", "Can't find the entered city")
        print(e)



"""
Runs a timer of 30mins to refresh the data
"""
def refresh_timer():
    try:
        #Intialize the timer for 30mins
        mins.set('30')
        secs.set('00')
        #calculate the number of iterations for updating the timer UI
        times = int(mins.get())*60 + int(secs.get())
        while times > -1:
            minute,second = (times // 60 , times % 60)
            hour =0
            if minute > 60:
                minute = minute % 60
            #Update the timer UI
            secs.set(str(second).zfill(2))
            mins.set(minute)
            #Update the time
            lable_mins.update()
            lable_secs.update()
            #wait for 1 second before the next iteration
            #so that it synchronizes with the actual waiting time
            time.sleep(1)
            if(times == 0):
                secs.set('00')
                mins.set('00')
            times -= 1
        #Refresh the data once the timer of 30mins runs out
        get_weather(cityw)
    except Exception as e:
        print("Exception handled")

#Search box
text_field_city = tk.Entry(root, justify="center", width=25, font=("arial",20), bg = "#42C2FF")
text_field_city.place(x=60, y=20)
text_field_city.focus()

#Search icon
search_icon = PhotoImage(file='search_icon.png',height=35, width=40)
search_button = Button(image=search_icon, justify=CENTER, cursor="hand2", bg = "#B8FFF9", borderwidth=0, command=get_weather)
search_button.place(x = 440, y = 20)

#Weather icon
status_icon = PhotoImage(file='status_icon.png',height=60, width=60)
lable_status_icon = Label(image= status_icon, borderwidth=0, bg='#B8FFF9')
lable_status_icon.place(x = 40, y = 90)

#displays the city
lable_city = Label(root, font = ("Arial", 15), bg = '#B8FFF9')
lable_city.place(x=100, y = 100)

#displays the current temperature
lable_current_temp = Label(root, font = ("Arial", 40), bg = '#B8FFF9')
lable_current_temp.place(x=40, y = 140)

#Displays the weather condition
lable_status = Label(root, font = ("Arial", 15), bg = '#B8FFF9')
lable_status.place(x = 40, y = 200)

#Wind lable
lable_wind = Label(root, text= "Wind:", font = ("Arial", 12), bg = '#B8FFF9')
lable_wind.place(x = 40, y = 250)

#wind value
lable_wind_value = Label(root, font = ("Arial", 12), bg = '#B8FFF9')
lable_wind_value.place(x = 90, y = 250)

#Humidity lable
lable_Humidity = Label(root, text= "Humidity:", font = ("Arial", 12), bg = '#B8FFF9')
lable_Humidity.place(x = 250, y = 250)

#Humidity value
lable_Humidity_value = Label(root, font = ("Arial", 12), bg = '#B8FFF9')
lable_Humidity_value.place(x = 320, y = 250)

#Timer
lable_timer = Label(root, text="Data will be updated in :", bg = "#B8FFF9", font = ("Arial", 12))
lable_timer.place(x = 400, y = 120)
#variables for maintaing minutes and seconds
mins = StringVar()
mins.set('30')
secs = StringVar()
secs.set('00')

#Display the minutes
lable_mins = Label(root, textvariable=mins, width=2, font = ('Helvetica',14), bg = "#85F4FF")
lable_mins.place(x = 425, y = 150)
lable_min_text = Label(root, text = "min.", font = ('Helvetica',10), bg = "#B8FFF9").place(x = 425, y = 175)

#Display the : for seperating minutes and seconds
lable_sep = Label(root, text=":", width=3, font = ('Helvetica',13), bg = "#85F4FF")
lable_sep.place(x = 450, y = 150)

#Display the seconds
lable_secs = Label(root, textvariable=secs, width=2, font = ('Helvetica',14), bg = "#85F4FF")
lable_secs.place(x = 475, y = 150)
lable_sec_text = Label(root, text = "sec.", font = ('Helvetica',10), bg = "#B8FFF9").place(x = 475, y = 175)

# Call the method to intialize the application
# with sarnia as the default input
get_weather()

root.mainloop()