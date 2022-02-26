from nanpy import ArduinoApi
from nanpy import SerialManager
from time import *
import requests
import math
temp = []
light = []
humid = []
moist = []
pointdelay = 0
while True:
    try:
        connection = SerialManager(device='COM3')
        a = ArduinoApi(connection=connection)
        a.pinMode(54, a.INPUT)
        a.pinMode(55, a.INPUT)
        a.pinMode(56, a.INPUT)

        while True:
            temp = round((1.0/((math.log(1023.0/a.analogRead(56)-1.0))/4275+1/298.15)-273.15),2)
            light = a.analogRead(54)
            humid = a.analogRead(57)
            moist = a.analogRead(55)
            print(temp)
            print(light)
            print(humid)
            print(moist)
            print('')
            try:
                requests.post('http://192.168.10.243:5000/update_plant', json={'temp':temp,'light':light,'humid':humid,'moist':moist})
            except:
                print("server not detected")
            sleep(5)
    except:
        print("arduino not connected")

