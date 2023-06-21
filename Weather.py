# Importing required library and files
import RPi.GPIO as GPIO
from email_new  import snd_email
from time import sleep
import drivers
import requests
from keyfile import runn
import pyttsx3


# Set up GPIO mode for led
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)


# Define pin numbers for VRX, VRY, and SW Joystick
VRX_PIN = 17
VRY_PIN = 27
SW_PIN = 22

# Set VRX and VRY pins as analog inputs ans SW_PIN for button
GPIO.setup(VRX_PIN, GPIO.IN)
GPIO.setup(VRY_PIN, GPIO.IN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Initalizing and setting properties for speaker
engine = pyttsx3.init()
engine.setProperty('engine', 'flite')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)


#lcd display method
display = drivers.Lcd()

#Main method for data 
def get_weather_and_humidity(country):
    api_key = 'ee5696d5565f9607a0ee20de76d5aea9'  #API Key
    base_url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {'q': country, 'appid': api_key, 'units': 'metric'}
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        #destructuring data from returned response
        if response.status_code == 200:
            weather = data['weather'][0]['description']
            humidity = data['main']['humidity']
            temp = data['main']['temp']
            wind = data['wind']['speed']
            icon= data['weather'][0]['icon']
            return weather, humidity ,temp ,wind,icon
        
        else:
            print('Error:', data['message'])
            return None
        
    except requests.RequestException as e:
        print('Request Error:', str(e))
        return None



# Define the available options of countries
options= ['London-UK','Washington-US','Rome-Italy','Valletta-Malta','Berlin-Germany'
            ,'Paris-France','Madrid-Spain','Beijing-China','Moscow-Russia','Tokyo-Japan']

#Logic for moving the joystick forward and backwards
current_option = 0
move_forward = False
move_backward = False

def select_option(forward=True):
    global current_option
    if forward:
        current_option = (current_option + 1) % len(options)
    else:
        current_option = (current_option - 1) % len(options)
    to_display=options[current_option]
    if len(to_display) < 16:
        num_spaces = 16 - len(to_display)
        to_display +=  ' ' * num_spaces
    display.lcd_display_string(to_display,1)
    display.lcd_display_string('press to select ',2)
    print("Selected:", options[current_option])

try:
    display.lcd_display_string("Welcome to Prj", 1)
    display.lcd_display_string("Move Joystick", 2)
    sleep(1)
    while True:
        # Read the values from VRX, VRY, and SW pins
        vrx_value = GPIO.input(VRX_PIN)
        vry_value = GPIO.input(VRY_PIN)
        sw_value = GPIO.input(SW_PIN)

        # Check joystick movement for option selection
        if vrx_value == 0 and vry_value == 1:
            move_forward = True
            move_backward = False
        elif vrx_value == 1 and vry_value == 0:
            move_backward = True
            move_forward = False
        elif vrx_value == 1 and vry_value == 1:
            if move_forward:
                display.lcd_clear()
                select_option(forward=True)
                move_forward = False
            elif move_backward:
                display.lcd_clear()
                select_option(forward=False)
                move_backward = False

        # Checking if the joystick is pressed 
        if sw_value == 0:
            display.lcd_display_string('    Waiting    ',1)
            display.lcd_display_string('      !!!      ',2)
            display.lcd_clear() 
            result=get_weather_and_humidity(options[current_option].split('-')[0])
            sleep(2)
            # Display the wether info on screen
            if result:
                display.lcd_clear()
                weather, humidity ,temp,wind,icon= result
                GPIO.output(26,GPIO.HIGH)
                runn(weather,humidity,temp,wind,str(icon),options[current_option])
                display.lcd_clear()
                GPIO.output(26,GPIO.LOW)
                display.lcd_display_string('Condition :     ',1)
                display.lcd_display_string(str(weather),2)
                engine.say("Its currently " +  str(weather) + "in" + str(options[current_option]))
                engine.runAndWait()
                sleep(2)
                display.lcd_clear() 
                display.lcd_display_string('Temperature : ',1)
                display.lcd_display_string(str(temp)+ '°C',2 )
                engine.say("The temperature is"+ str(temp) + "degree centigrade")
                engine.runAndWait()
                sleep(2)
                display.lcd_clear() 
                display.lcd_display_string('Humidity : ',1)
                display.lcd_display_string(str(humidity) + '%',2)
                engine.say("Humidity is"+ str(humidity))
                engine.runAndWait()
                sleep(2)
                display.lcd_clear() 
                display.lcd_display_string('Wind Speed : ',1)
                display.lcd_display_string(str(wind) + 'm/s',2)
                engine.say("And the wind speed  is"+ str(wind)+ "meter per second")
                engine.runAndWait()
                sleep(2)
                display.lcd_clear() 
                print(f"Weather : {weather}")
                print(f"Humidity  : {humidity}%")
                print(f"Temperature  : {temp}°C")
                print(f"Wind  : {wind} m/s")
            
except KeyboardInterrupt:
    GPIO.cleanup()