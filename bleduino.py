#! /usr/bin/python
from time import sleep

import subprocess
import traceback
import RPi.GPIO as GPIO
import serial
import threading
import sys
import os

#Functions to check power is on. 
from ads1x15_ex_singleended import check_adc_usb_on
from ads1x15_ex_singleended import check_adc_vin_on
from ads1x15_ex_singleended import check_adc_5v_on
from ads1x15_ex_singleended import check_adc_3v_on

#Functions to check power is off. 
from ads1x15_ex_singleended import check_adc_usb_off
from ads1x15_ex_singleended import check_adc_vin_off
from ads1x15_ex_singleended import check_adc_5v_off
from ads1x15_ex_singleended import check_adc_3v_off

#Functions to check led is on. 
from ads1x15_ex_singleended import check_adc_led	
	
def setup_test():
	try:
		logfunc("\n\nStarting setup-test\n")
		setup_gpio()
#		setup_serial()
		logfunc("Finished setup-test\n")
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-test\n")
		logfunc(result)
		logfunc("DONE -----------------------------------\n\n\n")
		finish_test(0)

def setup_gpio():
	try:
		logfunc(">> Starting setup-gpio\n")		
		#Configuring GPIOs
		GPIO.cleanup()
		GPIO.setmode(GPIO.BCM)
		logfunc(">>> Set GPIOs\n")
		
		GPIO.setup(4, GPIO.IN) #Firmware checksum
#		GPIO.setup(7, GPIO.IN) #Reset SPI
#		GPIO.setup(9, GPIO.IN) #MISO SPI
#		GPIO.setup(10, GPIO.IN) #SCK SPI
#		GPIO.setup(11, GPIO.IN) #MOSI SPI
		GPIO.setup(14, GPIO.IN) #TXD Pin
		GPIO.setup(15, GPIO.IN) #RXD Pin
		GPIO.setup(17, GPIO.OUT) #Power relay, 9V
		GPIO.setup(18, GPIO.OUT) #Power relay, USB
		GPIO.setup(22, GPIO.OUT) #Green (pass) result LED
		GPIO.setup(23, GPIO.OUT) #Red (fail) result LED
		logfunc(">>> Configured all GPIOs\n")
			
		#Reset result LEDs.
		GPIO.output(22, GPIO.LOW) #Green off.
		GPIO.output(23, GPIO.LOW) #Red off.
		logfunc(">>> Reseted green/red GPIOs\n")		
		logfunc(">> Finished setup-gpio\n")
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-gpio\n")
		logfunc(result)	
		logfunc("DONE -----------------------------------\n\n\n")			
		finish_test(0)

def setup_spi():
	try:
		logfunc(">> Starting setup-spi\n")		
		#Configuring GPIOs
#		GPIO.setmode(GPIO.BCM)
		logfunc(">>> Set SPIs\n")
		GPIO.setup(7, GPIO.IN) #Reset SPI
#		GPIO.setup(9, GPIO.IN) #MISO SPI
#		GPIO.setup(10, GPIO.IN) #SCK SPI
#		GPIO.setup(11, GPIO.IN) #MOSI SPI
		logfunc(">>> Configured all SPIs\n")
			
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-spi\n")
		logfunc(result)	
		logfunc("DONE -----------------------------------\n\n\n")			
		finish_test(0)
		
def setup_serial():	
	try:
		logfunc(">> Starting setup-serial\n")			
		#Configure Serial
		global ser
		ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
		ser.close()
		ser.open()	
		logfunc(">>> Configured serial port (rx/tx)\n")
		logfunc(">> Finished setup-serial\n")		
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-serial\n")
		logfunc(result)			
		logfunc("DONE -----------------------------------\n\n\n")		
		finish_test(0)
			
def power_test():
	try:
		logfunc("\n\nStarting power-test\n")		
		power_vin()
		power_vusb()
		power_vusb_vin()
		logfunc("Finished power-test\n")		
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: power-test\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")			
		finish_test(0)
		
def power_vin():
	try:
		logfunc(">> Starting power-vin\n")		
		#Vin > On, testing Vin.
		GPIO.output(17, GPIO.HIGH)	
		logfunc(">>> Vin is powered on\n")		
		sleep(2)
		adc9v = check_adc_vin_on()
		sleep(.1)
		adc3v = check_adc_3v_on()
		sleep(.1)
		adc5v = check_adc_5v_on()
		sleep(.1)
		adcUSB = check_adc_usb_off()
		sleep(.1)
		values =  '>>> vin: ' + str(adc9v) + ' 3v: ' + str(adc3v) + ' 5v: ' + str(adc5v) + ' usb: ' + str(adcUSB) 
		logfunc(values)	
			
		if(not adc9v or not adc3v or not adc5v or not adcUSB):
			logfunc(">>> Power-vin unsuccesful\n")				
			#Power test was unsuccesful
			GPIO.output(17, GPIO.LOW)
			logfunc(">>> Vin is powered off\n")			
			finish_test(0)

		logfunc(">>> Power-vin succesful\n")		
		#Vin > Off
		GPIO.output(17, GPIO.LOW)
		logfunc(">>> Vin is powered off\n")	
		sleep(2)
		logfunc(">> Finished power-vin\n")		
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: power-vin\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")			
		finish_test(0)

def power_vusb():
	try:
		logfunc(">> Starting power-vusb\n")	
		#V-USB > On, testing V-USB.
		GPIO.output(18, GPIO.HIGH)
		logfunc(">>> Vusb is powered on\n")				
		sleep(2)
		
		adcUSB = check_adc_usb_on()
		sleep(.1)
		adc3v = check_adc_3v_on()
		sleep(.1)
		adc5v = check_adc_5v_on()
		sleep(.1)
		adc9v = check_adc_vin_off()
		sleep(.1)
		values =  '>>> vin: ' + str(adc9v) + ' 3v: ' + str(adc3v) + ' 5v: ' + str(adc5v) + ' usb: ' + str(adcUSB)		
		logfunc(values)	

		if(not adcUSB or not adc3v or not adc5v or not adc9v):
			logfunc(">>> Power-vusb unsuccessful\n")					
			#Power test was unsuccesful.
			GPIO.output(18, GPIO.LOW)
			logfunc(">>> Vusb is powered off\n")		
			finish_test(0)
		
		logfunc(">>> Power-vin successful\n")		
		logfunc(">> Finished power-vusb\n")				
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: power-vusb\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")			
		finish_test(0)

def power_vusb_vin():
	try:
		logfunc(">> Starting power-vusb-vin\n")	
		#Vin > On, testing Vin and V-USB.
		GPIO.output(17, GPIO.HIGH)
		logfunc(">>> Vusb-Vin is powered on\n")			
		sleep(2)
		
		adcUSB = check_adc_usb_on()
		sleep(.1)
		adc9v = check_adc_vin_on()
		sleep(.1)
		adc3v = check_adc_3v_on()
		sleep(.1)
		adc5v = check_adc_5v_on()
		sleep(.1)
		values =  '>>> vin: ' + str(adc9v) + ' 3v: ' + str(adc3v) + ' 5v: ' + str(adc5v) + ' usb: ' + str(adcUSB)		
		logfunc(values)	
		
		if(not adcUSB or not adc9v or not adc3v or not adc5v):
			logfunc(">>> Power-vusb-vin unsuccessful\n")				
			GPIO.output(17, GPIO.LOW)
			GPIO.output(18, GPIO.LOW)
			logfunc(">>> Vusb and Vin is powered off\n")			
			finish_test(0)

		logfunc(">>> Power-vin succesful\n")	
		#Vin > Off, leave V-USB On for all the testing.
		GPIO.output(17, GPIO.LOW)
		logfunc(">>> Vin is powered off, Vusb left on for test\n")			
		sleep(2)
		
		logfunc(">> Finished power-vusb\n")	
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: power-vusb-vin\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")		
		finish_test(0)	

def checkSubprocess(outStream, errStream):
	return 0
	
#Micro-B
def setup_microB():
	try:
		logfunc("\n\nStarting setup-microB\n")		
#		setup_microB_bootloader() #Deprecated.
		setup_microB_sketch()
		logfunc("Finished setup-microB\n")		
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-microB\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")		
		finish_test(0)
	
def setup_microB_bootloader():
	try:
		#Upload bootloader to microB (i.e. Atmega328p)
		bootloader_cmd = "sudo avrdude -c linuxspi -p m328p -P /dev/spidev0.0 -U efuse:w:0x05:m -U hfuse:w:0xDA:m -U lfuse:w:0xFF:m -U flash:w:bootloader-microB.hex -U lock:w:0x0F:m"
		subprocess.Popen(bootloader_cmd, shell=True)
		sleep(10) #P:see if we can remove seelp, by keeping track of subprocess progress
	except Exception, e: 
		result = traceback.format_exc()
		finish_test(0)
		#P: save error codes

def setup_microB_sketch():
	try:	
		logfunc(">> Starting setup-microB-sketch\n")	
		#Upload sketch to microB (i.e. Atmega328p)
		sketch_cmd = ["avrdude", "-c", "linuxspi", "-p", "m328p", "-P" "/dev/spidev0.0", "-U" "efuse:w:0x05:m", "-U" "hfuse:w:0xDA:m", "-U" "lfuse:w:0xFF:m", "-U" "flash:w:sketch-microB.hex", "-v", "-v", "-v"]
		p=subprocess.Popen(sketch_cmd, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
	
		logfunc(">>> Launched microB-sketch subprocess, waiting for it to finish\n")	
		while(p.poll() is None):
			pass #waiting for usb setup
		logfunc(">>> MicroB-sketch subprocess is done running\n")
		logfunc(">>>Starting AVRdude for MicroB Sketch.\n")
		#Errors?
		out, err = p.communicate()
		logfunc(out)
		logfunc("########################\n")
		logfunc(err)
		logfunc("########################\n")
		errResult = checkSubprocess(out, err)

		if(errResult):
			logfunc(">>> MicroB-sketch unsuccesful\n")
			finish_test(0)	
		
	
		logfunc(">>> MicroB-sketch succesful\n")			
		logfunc(">> Finished setup-microB-sketch\n")				
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-microB-sketch\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")			
		finish_test(0)

#Micro-A		
def setup_microA():
	#Uplaod code to microA (via Arduino A's SPI
	try:
		logfunc("\n\nStarting setup-microA\n")		
		setup_spi()		
		setup_microA_bootloader()
		sleep(1)
		setup_microA_sketch()
		logfunc("Finished setup-microA\n")		
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-microA\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")		
		finish_test(0)
	
def setup_microA_bootloader():
	try:
		logfunc(">> Starting setup-microA-bootloader\n")	
		#Upload bootloader to microA (i.e. Atmega32u4)
		bootloader_cmd = ["avrdude", "-c", "arduino", "-p", "atmega32u4", "-P", "/dev/ttyACM0", "-U", "efuse:w:0xCB:m", "-U", "hfuse:w:0xD8:m", "-U", "lfuse:w:0xFF:m", "-U", "lock:w:0x3F:m", "-U", "flash:w:/home/pi/bootloader-microA.hex", "-U", "lock:w:0x2F:m", "-v", "-v", "-v"]
		p = subprocess.Popen(bootloader_cmd, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
		
		logfunc(">>> Launched microA-bootloader subprocess, waiting for it to finish\n")	
		while(p.poll() is None):
			pass #waiting for usb setup
		logfunc(">>> MicroA-bootloader subprocess is done running\n")

		logfunc(">>>Starting AVRdude for MicroA Sketch.\n")
		#Errors?
		out, err = p.communicate()
		logfunc(out)
		logfunc("########################\n")
		logfunc(err)
		logfunc("########################\n")
		errResult = checkSubprocess(out, err)

		if(errResult):
			logfunc(">>> MicroA-bootloader unsuccessful\n")
			finish_test(0)	
			
		logfunc(">>> MicroA-bootloader successful\n")			
		logfunc(">> Finished setup-microA-bootloader\n")
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-microA-bootloader\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")		
		finish_test(0)
		
def setup_microA_sketch():	
	try:
		logfunc(">> Starting setup-microA-sketch\n")
		#Upload testing sketch
		p = subprocess.Popen(["avrdude", "-c", "avr109", "-p", "atmega32u4", "-P", "/dev/ttyACM1", "-b", "57600", "-U", "flash:w:sketch-microA.hex", "-v", "-v", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		logfunc(">>> Launched microA-sketch subprocess, waiting for it to finish\n")	
		while(p.poll() is None):
			pass #waiting for usb setup
		logfunc(">>> MicroA-sketch subprocess is done running\n")

		logfunc(">>>Starting AVRdude for MicroA Sketch.\n")
		#Errors?
		out, err = p.communicate()
		logfunc(out)
		logfunc("########################\n")
		logfunc(err)
		logfunc("########################\n")		
		errResult = checkSubprocess(out, err)

		if(errResult):
			logfunc(">>> MicroA-sketch unsuccesful\n")
			finish_test(0)	
			
		logfunc(">>> MicroA-sketch succesful\n")			
		logfunc(">> Finished setup-microA-sketch\n")
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: setup-microA-sketch\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")	
		finish_test(0)
		
def usb_test():
	try:
		logfunc("\n\nStarting usb-test\n")
		setup_microA_bootloader()
		logfunc(">>> MicroA bootloader for usb-test is done\n")	
		sleep(1)

		#Upload final sketch
		p = subprocess.Popen(["avrdude", "-c", "avr109", "-p", "atmega32u4", "-P", "/dev/ttyACM1", "-b", "57600", "-U", "flash:w:/home/pi/sketch-microA-final.hex", "-v", "-v", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		logfunc(">>> Launched usb-test subprocess, waiting for it to finish\n")	
		while(p.poll() is None):
			pass #waiting for usb setup
		logfunc(">>> USB-test subprocess is done running\n")

		logfunc(">>>Starting AVRdude for MicroA Final Sketch.\n")
		#Errors?
		out, err = p.communicate()
#		logfunc(out)
#		logfunc("########################\n")
#		logfunc(err)
#		logfunc("########################\n")
		errResult = checkSubprocess(out, err)

		if(errResult):
			logfunc(">>> USB-test unsuccesful, uploading sketch unsuccesful\n")
			finish_test(0)	
			
		logfunc(">>> Verifying usb-test by checking pin 13 of BLEduino\n")
		#Veify sketch was uploaded properly.
		sleep(2) 
		sketch = GPIO.input(4)
		print "Pin 13: ", sketch
		if(not sketch):
			
			logfunc(">>> USB-test unsuccesful, pin confirmation unsuccesful\n")
			finish_test(0)
			
		sleep(1) #Making sure BLE is disconnected.
		logfunc(">>> USB-test succesful\n")			
		logfunc("Finished usb-test\n")
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: usb-test\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")	
		finish_test(0)
		
def start_arduino_tests():
	try:
		logfunc("\n\nStarting arduino-tests\n")
#		global ser
#		ser.write('L') #Send start command to Arduino.
#		sleep(.01)
#		ArduinoPineleven = GPIO.input(14)
#		ArduinoPintwelve = GPIO.input(15)
		
		logfunc(">>> Launched arduino-tests, sent signal to arduino, waiting for it to finish\n")
		#Wait for Arduino to notify us tests are done. 
		notified = 0
#		garbage = ser.read()
#			while (ArduinoPineleven == 0 and ArduinoPintwelve == 0):
		while not notified:
			
			pin11input = GPIO.input(14)
			print "ArduinoPineleven: ", pin11input
			sleep(0.01)
			if(pin11input== 1):
				sleep(0.05)
				pin12input = GPIO.input(15)
				if(pin12input == 1):
					logfunc(">>> Arduino-tests is done running, finished succesfully\n")
					logfunc("Finished arduino-tests\n")
					notified = 1
				else:
					logfunc("Failure: arduino-tests, BLE test unsuccesful")
					notified = 1
					finish_test(0)	
									
#			response = ser.read()
#			sleep(.01)
#			logfunc("Response from Arduino: ")
#			print "response: ", response
			
#			logfunc("ArduinoPin11: ")
		
#			logfunc("ArduinoPin12: ")
#			print "ArduinoPintwelve: ", ArduinoPintwelve
#			if(arduinopineleven == 1 and arduinopintwelve == 1):
#				logfunc(">>> Arduino-tests is done running, finished succesfully\n")
#				logfunc("Finished arduino-tests\n")
#				notified = 1
#			if(arduinopineleven == 0 and arduinopintwelve == 1):
#				logfunc("Failure: arduino-tests, pin pattern unsuccesful")
#				notified = 1
#				finish_test(0)
#			if(arduinopineleven == 1 and arduinopintwelve == 0):
#				logfunc("Failure: arduino-tests, BLE test unsuccesful")
#				notified = 1
#				finish_test(0)
				
#				finish_test(1)
#			notified = ('D' == response) #Received `Done` command?
			#if('p' == response or 'b' == response): #Error?
				#if(response == 'p'):
					#logfunc("Failure: arduino-tests, pin pattern unsuccesful")
				#else:
					#logfunc("Failure: arduino-tests, BLE test unsuccesful")	
				#finish_test(0)
		
#		logfunc(">>> Arduino-tests is done running, finished succesfully\n")		

#		sleep(1)		
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: arduino-test\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")		
		finish_test(0)
		
def led_test(): #Deprecated.
	try:	
		#led on
		print 'led-test'
		led_check('P')
		led_check('L')
		led_check('B')
		led_check('T')
		led_check('R')
	except Exception, e: 
		result = traceback.format_exc()
		finish_test(0)	

def led_check(identifier):
	try:
		print 'led-check: ', identifier
		global ser
		global led_avg
		if(identifier is not 'P'):
			ser.write(identifier)
		
		sleep(1) #wait for led on
		led_on = check_adc_led(identifier)
		ser.write('O') #led off
		sleep(1) #wait for led off
		if(not led_on):
			finish_test(0) 
	except Exception, e: 
		result = traceback.format_exc()
		finish_test(0)	
		
def start_monitoring_ldo():
	try:
		global done
		logfunc("\n\nStarted: minotor-ldo-process\n")
		while not done:	
			adcUSB = check_adc_usb_on()
			adc9v = check_adc_vin_off()
			adc3v = check_adc_3v_on()
			adc5v = check_adc_5v_on()
			if(not adcUSB or not adc9v or not adc3v or not adc5v):
				logfunc("\n\Failure: minotor-ldo-process, unsuccesful\n")
				finish_test(0)
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: monitor-ldo process\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")			
		finish_test(0)
					
def monitor_ldo():
	try:
		logfunc("\n\nStarted: minotor-ldo-thread\n")		
		blink_thread = threading.Thread(target= start_monitoring_ldo)
		blink_thread.start()
		logfunc("Finished: minotor-ldo-thread\n")		
	except Exception, e: 
		result = traceback.format_exc()
		logfunc("********************************\n")		
		logfunc("********************************\n")
		logfunc("Failure: monitor-ldo-thread\n")
		logfunc(result)		
		logfunc("DONE -----------------------------------\n\n\n")			
		finish_test(0)
					
def finish_test(result):
	try:
		#Disable ldo monitoring thread
		global done
		done = True
		sleep(0.3)
		if(result):
			#Test-jig was succesful.
			GPIO.output(17, GPIO.LOW) #Power relay, 9V
			GPIO.output(18, GPIO.LOW) #Power relay, USB
			sleep(1)
			GPIO.output(22, GPIO.HIGH) #Green on.
			logfunc('All power sources have been powered off\n')
			logfunc('Bleduino test finished succesfully >>>')

		else:
			#Test-jig was unsuccesful.
			GPIO.output(17, GPIO.LOW) #Power relay, 9V
			GPIO.output(18, GPIO.LOW) #Power relay, USB
			sleep(1)
			GPIO.output(23, GPIO.HIGH) #Red on.	
			logfunc('All power sources have been powered off\n')			
			logfunc('Bleduino test finished unsuccesfully <<<')

		os._exit(0) #kill test.
	except Exception, e: 
		result = traceback.format_exc()
		os._exit(0) #kill test.

def logfunc(msg):
	try:
		out_file = open("/home/pi/Desktop/bleduino-log.txt","a")
		out_file.write(msg)
		out_file.close()
		print msg
	except Exception, e: 
		result = traceback.format_exc()
		print result

def backtest():
	try:
		logfunc('backtest-starting')
		setup_test()
		GPIO.setup(24, GPIO.OUT) #BLUE LED
		GPIO.output(24, GPIO.HIGH) #BLUE on.
		usb_test()
		finish_test(1)
	except:
		logfunc('backtest-failed')
		finish_test(0)
		
#Main thread
#Serial port	
ser = None
#LDO shutdown trigger
done = False

try:
	logfunc("\n\n#####################################\n")
	logfunc("#####################################\n")
	logfunc("Starting new BLEduino test:  \n")
	logfunc("#####################################\n")
	logfunc("#####################################\n")
	logfunc("Process: -----------------------------------\n")

	setup_test()
	power_test()
	monitor_ldo()
#	logfunc("Sleeping for 5 seconds.......\n")
#	sleep(10)
	setup_microB() 
	setup_microA()
	start_arduino_tests()
	usb_test()

	#All test completed succesfuly.
	finish_test(1)
except Exception, e: 
	result = traceback.format_exc()
	logfunc("********************************\n")		
	logfunc("********************************\n")
	logfunc("Failure: main-thread\n")
	logfunc(result)		
	logfunc("DONE -----------------------------------\n\n\n")
	finish_test(0)
	
