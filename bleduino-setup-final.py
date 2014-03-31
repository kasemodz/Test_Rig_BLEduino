#! /usr/bin/python
import RPi.GPIO as GPIO
import os
import subprocess 
import threading
import signal
from time import sleep

#Configuring GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.OUT) #Yellow (power/running) LED
GPIO.setup(23, GPIO.OUT) #Red (error) LED

proc = None
to_timer = None
gpid = None
blink_thread = None
yellow_state = False

def logfunc(msg):
	try:
		out_file = open("/home/pi/Desktop/bleduino-log.txt","a")
		out_file.write(msg)
		out_file.close()
		print msg
	except Exception, e: 
		result = traceback.format_exc()
		print result
	
#Kill bleduino test if it has run for over 90s. 
def kill_test(pid):
	global proc
	result = proc.poll()
	
	#Is the test still running?
	if(result is None and proc.pid == pid):
		logfunc("Failure: timeout has expired, BLEduino test will be killed")
		os.kill(pid, signal.SIGTERM) #Kill the test.
		GPIO.output(23, GPIO.HIGH) #Turn red LED on.		
		logfunc("BLEduino test has been killed")

#Start blinking yellow led. 
def blink_led():
	state = True
	while 1:
		GPIO.output(24, state) #Blink LED on.
		state = not state
		sleep(0.10)
			
#Launch bleduino test.
def bleduino_test(channel):
	global proc
	global to_timer
	global gpid
	
	if(GPIO.input(25) == True):
		#Is there a test running?
		if(proc is None):						
			#Launch bleduino test script.
			proc = subprocess.Popen(['sudo', 'python', '/home/pi/bleduino.py']) 
			gpid = proc.pid
		
			#Start timeout. 
			to_timer = threading.Timer(120, kill_test, [proc.pid])
			to_timer.start()

#Reset button interrupt.  
GPIO.add_event_detect(25, GPIO.RISING, callback=bleduino_test, bouncetime=5000)

#Monitor tests.
while 1:
	#Is there a test runing?
	if(proc is not None):
		GPIO.output(24, yellow_state) #toglle yellow led
		yellow_state = not yellow_state 
		result = proc.poll()
		#Is the test finished?
		if(result is not None):
			#Get ready for next test.
			to_timer.cancel() #Cancel timeout.
			proc = None #Enable launching tests.
			GPIO.output(24, GPIO.HIGH) #Turn yellow LED on.
			sleep(.10)
		
	
