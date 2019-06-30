#!/usr/bin/python
import RPi.GPIO as GPIO
import grovepi
import math
import requests,json
import time
import firebase
import urllib
import smbus
import serial
import time
import paho.mqtt.client as mqtt


"""TOKEN = "A1E-NAZ9xIT16E1thMWYvc7Zph2SM2e16o"  # Put your TOKEN here
DEVICE_LABEL = "fd"  # Put your device label here 
VARIABLE_LABEL_1 = "touch"  # Put your first variable label here
VARIABLE_LABEL_2 = "pulse"  # Put your second variable label here"""
firebase=firebase.FirebaseApplication('https://able-dryad-244208.firebaseio.com/')



# Connect the Grove Temperature Sensor to analog port A0
# SIG,NC,VCC,GND
sensor = 0
grovepi.pinMode(sensor,"INPUT")
# Connect the Grove Gas Sensor to analog port A1
# SIG,NC,VCC,GND
gas_sensor = 1
grovepi.pinMode(gas_sensor,"INPUT")

# Connect the Grove Touch Sensor to digital port D5
# SIG,NC,VCC,GND
touch_sensor = 5
grovepi.pinMode(touch_sensor,"INPUT")
##

grovepi.pinMode(gas_sensor,"INPUT")
##
#Fire Flame Sensor GPIO SETUP
pulse_sensor = 3
grovepi.pinMode(pulse_sensor,"INPUT")

##serialCommunication with arduino
#ser= serial.Serial('/dev/ttyACM0',115200)

Broker = "59.162.178.178"
port = 1883

client = mqtt.Client()

#client.connect(Broker,port)

#topic = "device/5d04c8a6fe98512df03124a1"
print("------------------------------------------")
print("------------------------------------------")
print(" ")
print("HEALTHCARE MONITORING SYSTEM ")
print(" ")
print("------------------------------------------")
print("------------------------------------------")
while True:
    try:
        #serial communication with Arduino
        print ('Scanning sensors ....')
        print("------------------------------------------")
        """s = str(ser.readline())
        print(s)
        x=s.split("|")[0]
        x1=x.split("'")[1]
        y=s.split("|")[1]
        y1=y.split("\\")[0]
        print("")
        print("CO2    : ",x1,"PPM")
        print("----------------------------------------------")
        print("")
        print("Pulse  : ",y1,"BPM")
        print("----------------------------------------------")
        print("")"""

            

##
        #Flame Sensor
        """flame = grovepi.digitalRead(flame_sensor)
        if flame==0 or flame==1:	
            if flame==0:
                print ('Flame : Detected')
                print("----------------------------------------------")
                print("")

            else:
                print ('Flame : Not Detected')
                print("----------------------------------------------")
                print("")"""

    	# This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        temp = grovepi.temp(sensor,'1.1')
        print("Temperature : ", round(temp,2)," Degree Celcius")
        print("----------------------------------------------")
        print("")



        # Get touch sensor value
        touch = grovepi.digitalRead(touch_sensor)
        if touch==0 or touch==1:	
            if touch==1:
                print ('Touch : Detected')
                print("----------------------------------------------")
                print("")
            else:
                print ('Touch : Not Detected')
                print("----------------------------------------------")
                print("")
##

	#3-Axis Accelerometer Snesor
        print("Gyroscope Values")
        print("--------")
        Gyroscop_xout = read_word_2c(0x43)
        Gyroscop_yout = read_word_2c(0x45)
        Gyroscop_zout = read_word_2c(0x47)
       
        print(("Gyroscope_x_axis: "), ("%5d" % Gyroscop_xout), (" Scaled: "), round((Gyroscop_xout / 131),2))
        print(("Gyroscope_y_axis: "), ("%5d" % Gyroscop_yout), (" Scaled: "), round((Gyroscop_yout / 131),2))
        print(("Gyroscope_z_axis: "), ("%5d" % Gyroscop_zout), (" Scaled: "), round((Gyroscop_zout / 131),2)) 
        print()
        print("Acceleration Values")
        print("---------------------")
        acceleration_xout = read_word_2c(0x3b)
        acceleration_yout = read_word_2c(0x3d)
        acceleration_zout = read_word_2c(0x3f)
         
        acceleration_xout_scaled = acceleration_xout / 16384.0
        acceleration_yout_scaled = acceleration_yout / 16384.0
        acceleration_zout_scaled = acceleration_zout / 16384.0
         
        
        print ("Acceleration_x_axis: ", ("%6d" % acceleration_xout), (" Scaled: "), round(acceleration_xout_scaled,2))
        print ("Acceleration_y_axis: ", ("%6d" % acceleration_yout), (" Scaled: "), round(acceleration_yout_scaled,2))
        print ("Acceleration_z_axis: ", ("%6d" % acceleration_zout), (" Scaled: "), round(acceleration_zout_scaled,2))
        print()
        print("Rotation Values")
        print("---------")
        x_rotation = get_x_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        y_rotation = get_y_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled)
        print("Rotation of x-axis : ",round(x_rotation,2))     
        print("Rotation of y-axis : ",round(y_rotation,2))
        print("---------------------")
        print("")
##
            pulse=grovepi.analogRead(pulse_sensor)
            print("pulse value--",pulse)
##
        # Get gas sensor value
        gas = grovepi.analogRead(gas_sensor)
        # Calculate gas density - large value means more dense gas
        density = (float)(gas / 1024)
        print("Gas Sensor Value : ", gas, "PPM, Density : ", round(density,2))
        print("----------------------------------------------")
        print("")
        flame=100
        co2=100
        """data = json.dumps([{"sensor" : "temperature", "value":temp, "timestamp":"","context":"Temperature:Celsius"},
                       {"sensor": "gas-sensor",  "value":gas, "timestamp":"","context":"Gas:PPM"},
                       {"sensor": "touch-sensor",  "value":touch, "timestamp":"","context":"Touch:No|Yes"},
                       {"sensor": "pulse-sensor",  "value":pulse, "timestamp":"","context":"Pulse:PPM"},
                       {"sensor": "fire-flame-sensor",  "value":flame, "timestamp":"","context":"Flame:No|Yes"}, 
                       {"sensor": "co2-sensor",  "value":co2, "timestamp":"","context":"Co2:PPM"}])"""
        result=firebase.post('https://able-dryad-244208.firebaseio.com/',{'pulse':str(pulse),'touch':str(touch),'timestamp':time})
        print("")
        #client.publish(topic,data)
        
        print("------------------------------------------")
        print("------------------------------------------")
        print(" ")
        print("Data uploaded ")
        print(" ")
        print("------------------------------------------")
        print("------------------------------------------")
        time.sleep(5)

    except IOError:
        print ("Error")

