"""
This is assuming DuPlessie MiniMac, position control NOT velocity control (for now)
Using mode 4 (16 bit, 10 channels) -> refer to manual to understand how to get to mode

Pan is 540 degrees, tilt is 270 degrees
Pan resolution is 0.013 degrees, tilt resolution is 0.007 degrees

Relevant Channels (Mode 4)
[5] pan (0 is left, 255 is right, 128 is neutral)
[6] pan fine (0 is left, 255 is right)
[7] pan (0 is up, 255 is down, 128 is neutral)
[8] pan fine (0 is up, 255 is down)
[9] pan/tilt speed
	0 - 2: tracking mode
	3 - 245: fast to slow
	246 - 248: tracking, PtS = SLO
	249 - 251: tracking, PtS = FST
	252 - 255: black out while moving

Currently NOT in a loop, just runs once
"""

import pysimpledmx # make sure it is in same home directory

COMport = "/dev/ttyUSB0" # define COMport number

mydmx = pysimpledmx.DMXConnection(COMport) # create dmx object

# assuming that we are getting pan angle and tilt angle, make sure we're getting floats!
pAngle = 30.0
tAngle = 30.0

# math for turning "real angles" into DMX values
pAnglePercentage = pAngle/540
tAnglePercentage = tAngle/270

pAngleDMX = round(pAnglePercentage*65535) 
tAngleDMX = round(tAnglePercentage*65535) 

pAngleDMX 
tAngleDMX

# for reals sending values to DMX

mydmx.setChannel(1, 255) # set DMX channel 1 to full
mydmx.setChannel(2, 128) # set DMX channel 2 to 128
mydmx.setChannel(3, 0) # set DMX channel 3 to 0
mydmx.render() render # render all of the above changes onto the DMX network

mydmx.setChannel(4, 255, autorender=True) # set channel 4 to full and render to the network

