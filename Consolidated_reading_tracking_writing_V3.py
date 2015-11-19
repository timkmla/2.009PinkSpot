import math
import serial 
from time import sleep



def distance(one, two):
    return ((one[0]-two[0])**2 + (one[1]-two[1])**2 + (one[2]-two[2])**2)**.5

def LawofCosines(Aop,Bop,Cop):
    return math.acos((Aop**2 + Bop**2 - Cop**2)/ (2 * Aop * Bop) )

def Loc_3D(dist_ta_a0, dist_ta_a1, dist_ta_a2, Loc_1, Loc_2):
    """
    Uses Trilateration to return 3 coordinate points from Anchor position and distances

    """
    Position = []
    Position.append((dist_ta_a0**2 - dist_ta_a1**2 + Loc_1[0]**2)/ (2*Loc_1[0]))
    Position.append((dist_ta_a0**2 - dist_ta_a2**2 - Position[0]**2 +(Position[0]-Loc_2[0])**2 + Loc_2[1]**2)/(2*Loc_2[1]))

    #To avoid square rooting negative number when z = 0, but range of tracking error gives small negative value under intercept
    if (dist_ta_a0**2 - Position[0]**2 - Position[1]**2) >= 0 :
        
        Position.append((dist_ta_a0**2 - Position[0]**2 - Position[1]**2)**.5)
    else :
        Position.append(0)
            
    return Position 
    
##########################################################################################

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 17:20:35 2015

@author: Katie, Joy

reading_data code reads distances between the tag and each anchor.

install pyserial to run the code. go to the link below to install:
https://learn.adafruit.com/arduino-lesson-17-email-sending-movement-detector/overview

"""

##########################################################################
#user defined variables: port, count_average, num_output 

#serial port address. Windows uses 'COM1', 'COM2'.. 
#but MAC uses different types of address. 
port = "COM7"
motor_port = "COM13"

# calculate and output an average of distances every 'count_average' distance measurings
count_average = 10 

# The total number of outputs. 
# (count_average * num_ouput) is the total number of measurings
num_output = 30

#########################################################################


count = 0 #start counting
dist_ta_a0 = 0 
dist_ta_a1 = 0 
dist_ta_a2 = 0 
dist_a0_a1 = 0 
dist_a0_a2 = 0
dist_a1_a2 = 0 

ser  = serial.Serial(port, 9600, timeout= 0 ) #start the serial port communication
ser_motor = serial.Serial(motor_port, 9600)

#############################################################################
#print 'zeroing anchor distances' 
countupto = 30 #recording up to 10 times. You can change the number
dist0 = [] 
dist1 = []
dist2 = []

while count < countupto:   
    count += 1 
    data = ser.read(9999)
    if len(data) > 0 :
        if data[0:2] == 'ma': # 'ma' means the distances between anchors 
            dist0.append( int(data[15:23], 16)) #bw anchor 0 and 1 
            dist1.append( int(data[24:32], 16)) #bw anchor 0 and 2
            dist2.append( int(data[33:41], 16)) #bw anchor 1 and 2
    else:
        print "no data"
    sleep(0.5) # collect the data every 0.5 seconds 
#Calculate the averages of ten continuous distances and print them out 
dist_a0_a1 = float( sum(dist0) ) / len(dist0) 
dist_a0_a2 = float( sum(dist1) ) / len(dist1)
dist_a1_a2 = float( sum(dist2) ) / len(dist2)

##print len(dist0)
##print len(dist1)
##print len(dist2) 
##
##print 'dist_a0_a1: ', dist_a0_a1
##print 'dist_a0_a2: ', dist_a0_a2
##print 'dist_a1_a2: ', dist_a1_a2

#############################################################################
## IDENTIFYING ANCHOR POSITIONS

##Anchor 0 Bottom left corner
##Anchor 1 Bottom right corner
##Anchor 2 Top left corner, --> 0-1-2 must be oriented so +z is upward
Loc_0 = [0,0,0]
Loc_1 = [dist_a0_a1, 0, 0]

Angle_012 = LawofCosines(dist_a0_a1, dist_a1_a2, dist_a0_a2) 
y = dist_a1_a2 * math.sin(Angle_012)
x = dist_a1_a2 * math.cos(Angle_012)

## If anchors set up as shown above, double points shouldn't be an issue
## However, ** Anchor 2 to the right of Anchor 1 issue
Loc_2 = [dist_a0_a1 - x, y, 0]

print ''
print "Location of 1st anchor: " + str(Loc_0)
print "Location of 2nd anchor: " + str(Loc_1)
print "Location of 3rd anchor: " + str(Loc_2)



###########################################################################################
## LIGHT POSITION CALIBRATION
##    Light_Location = []
##    TAG_0 = float(raw_input("Light_TAG_0: "))
##    TAG_1 = float(raw_input("Light_TAG_1: "))
##    TAG_2 = float(raw_input("Light_TAG_2: "))
##
##    Light_Location.append((TAG_0**2 - TAG_1**2 - Loc_1[0]**2)/ (2*Loc_1[0]))
##    Light_Location.append((TAG_0**2 - TAG_2**2 - Loc_2[0]**2 + Loc_2[1]**2)/(2*Loc_2[1]) - Loc_2[0] * Light_Location[0]/ Loc_2[1])
##    Light_Location.append((TAG_0**2-Light_Location[0]**2-Light_Location[1]**2)**.5)
##Light_Location = [1952.126246752051, 534.2969281540112, 864.9456106062033]
##print "Light Location"
##print Light_Location

############################################################################################
##LIGHT ORIENTATION CALIBRATION! UNFINISHED
## Transforming between 2 spherical coordinate systemss


############################################################################################

print 'measuring anchor to anchor distances '
#, num_output, 'times'
count = 0 
dist0 = [] 
dist1 = []
dist2 = []
# Will locate until told to stop

locate_again =  "y"
light_found = "n"

#print ser_motor.readline()
while count < count_average * num_output :
#while locate_again == 'y':
    count += 1 
    data = ser.read(9999)
    if len(data) > 0 :
        ##### for debugging only. Printing the whole data 
##        print data    
        if data[0:2] == 'mc':    
##            print 'getting data' 
            dist0.append( int(data[6:14], 16) ) #bw tag and anchor 0
            dist1.append( int(data[15:23], 16) ) #bw tag and anchor 1
            dist2.append( int(data[24:32], 16) ) #bw tag and anchor 2

    if len(dist0) != 0 and len(dist1) != 0 and len(dist2) != 0:
        if count !=  0 and count % count_average == 0 :
            dist_ta_a0 = float( sum( dist0 ) ) / len(dist0)
            dist_ta_a1 = float( sum( dist1 ) ) / len(dist1)
            dist_ta_a2 = float( sum( dist2 ) ) / len(dist2)
            dist0 = [] 
            dist1 = []
            dist2 = []
            ##### for debugging only. Printing out the distances 
##            print 'count :', count
##            print 'dist_ta_a0 :', dist_ta_a0    
##            print 'dist_ta_a1 :', dist_ta_a1    
##            print 'dist_ta_a2 :', dist_ta_a2
            ###### Finding Light
            if count / count_average == 1:
                Light_Location = Loc_3D(dist_ta_a0, dist_ta_a1, dist_ta_a2, Loc_1, Loc_2)                
                print "Our Light location"
                print Light_Location
                light_found = raw_input("Light is found! Move Tag to tracking location. (enter y when ready): ")
                
            
            elif light_found == "y":
                ##POSITION TRACKING - Trilateration
                Our_Space_Point = Loc_3D(dist_ta_a0, dist_ta_a1, dist_ta_a2, Loc_1, Loc_2)
                
                ## PAN-TILT, Tilt 0 -> (0,0,-z), Pan 0 -> (-x ,0 ,0) for light behind point, (x,0,0) for light in front of point. 

                ## Light behind Tag
                if Our_Space_Point[1] >= Light_Location[1]:
                    Model_Tilt = math.acos((Light_Location[2]- Our_Space_Point[2]) /distance(Light_Location, Our_Space_Point))
                    if  Our_Space_Point[0] >= Light_Location[0] :
                        Model_Pan = math.pi - math.atan((Our_Space_Point[1] - Light_Location[1]) / (Our_Space_Point[0]  - Light_Location[0] ))
                    else:
                        Model_Pan = math.atan((Our_Space_Point[1] - Light_Location[1]) / (Light_Location[0] - Our_Space_Point[0]  ))
                ## Light infront of Tag
                else:
                    Model_Tilt = Model_Tilt
                    Model_Pan = Model_Pan


                #Angle into String and setting len of string = 3 
                Tilt_Angle = str(int(Model_Tilt*360.0/(2*math.pi)))
                Pan_Angle = str(int(Model_Pan*360.0/(2*math.pi)))
                
                if len(Tilt_Angle) == 2:
                    Tilt_Angle = '0'+ Tilt_Angle

                if len(Tilt_Angle) == 1:
                    Tilt_Angle = '00'+ Tilt_Angle

                if len(Pan_Angle) == 2:
                    Pan_Angle = '0' + Pan_Angle
                    
                if len(Pan_Angle) == 1:
                    Pan_Angle = '00'+ Pan_Angle

                print '255' + Tilt_Angle + Pan_Angle

                ser_motor.write('255' + Tilt_Angle + Pan_Angle)
                
#                locate_again = raw_input("Again? (y or n): ")

        

    sleep(0.2) # collect the data every 0.2 seconds 

ser_motor.write('255000000')    
ser.close() #end the communication

#print "Done tracking"



##########################################################################################



























