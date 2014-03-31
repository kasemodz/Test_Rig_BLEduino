#!/usr/bin/python

import time, signal, sys
from Adafruit_ADS1x15_1 import ADS1x15_GND
from Adafruit_ADS1x15_2 import ADS1x15_VDD


#import time, signal, sys
#from Adafruit_ADS1x15_2 import ADC_2

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

ADS1015 = 0x00  # 12-bit ADC
#ADS1115 = 0x01	# 16-bit ADC

# Select the gain
gain = 6144    # +/- 6.144V
#gain = 4096  # +/- 4.096V
#gain = 2048  # +/- 2.048V
#gain = 1024  # +/- 1.024V
#gain = 512   # +/- 0.512V
gain_current = 256   # +/- 0.256V


# Select the sample rate
#sps = 8    # 8 samples per second
#sps = 16   # 16 samples per second
#sps = 32   # 32 samples per second
#sps = 64   # 64 samples per second
#sps = 128  # 128 samples per second
#sps = 250  # 250 samples per second
#sps = 475  # 475 samples per second
sps = 860  # 860 samples per second
sps_current = 3300  # 3300 samples per second

# Initialise the ADC using the default mode (use default I2C address)

# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
#adc = ADS1x15(ic=ADS1015)

margin = 0.5

adc0 = ADS1x15_VDD(ic=ADS1015)
adc1 = ADS1x15_GND(ic=ADS1015) 

# Read channel 0 in single-ended mode using the settings above


volts_adc1_gnd = adc0.readADCSingleEnded(1,gain,sps) / 1000
print volts_adc1_gnd
#Functions to check power is on.
def check_adc_usb_on():
	try:
		global margin
		volts_adc0_usb = adc0.readADCSingleEnded(0, gain, sps) / 1000
#		print 'usb-value: ',volts_adc0_usb
		
		max_value = 5+margin
		min_value = 5-margin
		if(volts_adc0_usb >= min_value and volts_adc0_usb <= max_value):
			return True
		return False
	except:
		return False
	
def check_adc_vin_on():
	try:
		global margin
		volts_adc0_vin = adc0.readADCSingleEnded(1,gain,sps) / 1000
#		print 'vin-value: ',volts_adc0_vin
		
		max_value = 5+margin
		min_value = 5-margin
		if(volts_adc0_vin >= min_value and volts_adc0_vin <= max_value):
			return True
		return False
	except:
		return False
	
def check_adc_5v_on():
	try:
		global margin
		volts_adc0_5v = adc0.readADCSingleEnded(2,gain,sps) / 1000
#		print '5v-value: ',volts_adc0_5v
		
		max_value = 5+margin
		min_value = 5-margin
		if(volts_adc0_5v >= min_value and volts_adc0_5v <= max_value):
			return True		
		return False
	except:
		return False
	
def check_adc_3v_on():
	try:
		global margin
		volts_adc0_3v = adc0.readADCSingleEnded(3, gain, sps) / 1000
#		print '3v-value: ',volts_adc0_3v
		
		max_value = 3.3+margin
		min_value = 3.3-margin
		if(volts_adc0_3v >= min_value and volts_adc0_3v <= max_value):
			return True
		return False
	except:
		return False
	
#Functions to check power is off. 
def check_adc_usb_off():
	try:
		global margin
		volts_adc0_usb = adc0.readADCSingleEnded(0, gain, sps) / 1000
#		print 'usb-value-off: ',volts_adc0_usb
		
		max_value = 0+margin
		min_value = 0-margin
		if(volts_adc0_usb >= min_value and volts_adc0_usb <= max_value):
			return True
		return False
	except:
		return False
	
def check_adc_vin_off():
	try:
		global margin
		volts_adc0_vin = adc0.readADCSingleEnded(1,gain,sps) / 1000
#		print 'vin-value-off: ',volts_adc0_vin
		
		max_value = 0+margin
		min_value = 0-margin
		if(volts_adc0_vin >= min_value and volts_adc0_vin <= max_value):
			return True
		return False
	except:
		return False
	
def check_adc_5v_off():
	try:
		global margin
		volts_adc0_5v = adc0.readADCSingleEnded(2,gain,sps) / 1000
		print '5v-value-off: ',volts_adc0_5v
		
#		max_value = 0+margin
#		min_value = 0-margin
		if(volts_adc0_5v >= min_value and volts_adc0_5v <= max_value):
			return True		
		return False
	except:
		return False
	
def check_adc_3v_off():
	try:
		global margin
		volts_adc0_3v = adc0.readADCSingleEnded(3, gain, sps) / 1000
#		print '3v-value-off: ',volts_adc0_3v
		
		max_value = 0+margin
		min_value = 0-margin
		if(volts_adc0_3v >= min_value and volts_adc0_3v <= max_value):
			return True
		return False
	except:
		return False
	
	

#Functions to check led is on.	
def check_adc_led(identifier):
	try:
		global gain_current
		volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
		current = (volts_adc1_gnd / 1.5) * 1000
		print 'current value: ',current
		
		if(identifier == 'P'):
#			return (current >= 41.1776 and current <=41.4823)
			if(current < 40.0  or current > 41.5):
				print 'Nigga I be tryin this shit again, it better work.'
				volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
				current = (volts_adc1_gnd / 1.5) * 1000
				print '2nd Try current value: ',current	
				if(current < 40.0  or current > 41.5):
					print 'You are a grown man, stop cryin.'
					volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
					current = (volts_adc1_gnd / 1.5) * 1000
					print '3rd Try current value: ',current				
			return (current >= 40.0  and current <=41.5)	
#			return (current >= 40.83  and current <=41.83)
		elif(identifier == 'L'):
#			return (current >= 43.0139 and current <=43.1308)
			if(current < 42.5  or current > 43.75):
				print 'Nigga I be tryin this shit again, it better work.'
				volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
				current = (volts_adc1_gnd / 1.5) * 1000
				print '2nd Try current value: ',current	
				if(current < 42.5  or current > 43.75):
					print 'You are a grown man, stop cryin.'
					volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
					current = (volts_adc1_gnd / 1.5) * 1000
					print '3rd Try current value: ',current
			return (current >= 42.5 and current <=43.75)							
#			return (current >= 42.63 and current <=43.63)
		elif(identifier == 'B'):
#			return (current >= 42.4369 and current <=43.7431)
			if(current < 42.5  or current > 44.0):
				print 'Nigga I be tryin this shit again, it better work.'
				volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
				current = (volts_adc1_gnd / 1.5) * 1000
				print '2nd Try current value: ',current	
				if(current < 42.5  or current > 44.0):
					print 'You are a grown man, stop cryin.'
					volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
					current = (volts_adc1_gnd / 1.5) * 1000
					print '3rd Try current value: ',current			
			return (current >= 42.5 and current <=44.0)	
#			return (current >= 42.59 and current <=43.59)
		elif(identifier == 'T'):
#			return (current >= 43.2329 and current <=43.6470)
			if(current < 43.0  or current > 44.25):
				print 'Nigga I be tryin this shit again, it better work.'
				volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
				current = (volts_adc1_gnd / 1.5) * 1000
				print '2nd Try current value: ',current	
				if(current < 43.0  or current > 44.25):
					print 'You are a grown man, stop cryin.'
					volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
					current = (volts_adc1_gnd / 1.5) * 1000
					print '3rd Try current value: ',current	
			return (current >= 43.0 and current <=44.25)
#			return (current >= 42.94 and current <=43.94)
		elif(identifier == 'R'):
#			return (current >= 43.5644 and current <=44.1356)
			if(current < 43.5  or current > 45.0):
				print 'Nigga I be tryin this shit again, it better work.'
				volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
				current = (volts_adc1_gnd / 1.5) * 1000
				print '2nd Try current value: ',current	
				if(current < 43.5  or current > 45.0):
					print 'You are a grown man, stop cryin.'
					volts_adc1_gnd = adc1.readADCSingleEnded(0, gain_current, sps_current) / 1000
					current = (volts_adc1_gnd / 1.5) * 1000
					print '3rd Try current value: ',current	
			return (current >= 43.5 and current <=45.0)
#			return (current >= 43.35 and current <=44.35)
		else:
			return False
	except:	
		return False


#try:
#	test1 = check_adc_usb_off()	
#	print 'A0: '  "%.6f" % (test1)
#	print 'Be calm, shit be cool.'
#except:
print 'Shit aint working, fix it!'	

check_adc_vin_on()
check_adc_5v_on()
check_adc_3v_on()
check_adc_usb_on()
# To read channel 3 in single-ended mode, +/- 1.024V, 860 sps use:
# volts = adc.readADCSingleEnded(3, 1024, 860)
#print 'ADS1015-1 '
#print '----------'
#print 'A0: '  "%.6f" % (volts_adc1_gnd)
#print 'A0: '  "%.6f" % (volts_adc0_vin)
#print 'A0: '  "%.6f" % (volts_adc0_5v)
#print ' '

#print 'ADS1015-2 '
#print '----------'
#print 'A1: '  "%.6f" % (volts_adc1_3v)

