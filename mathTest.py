tAngle = float(90.1)

# math for turning "real angles" into DMX values
#pAnglePercentage = pAngle/540
tAnglePercentage = tAngle/270

#pAngleDMX = round(pAnglePercentage*65535) 
tAngleDMX = int(round(tAnglePercentage*65535))

#pAngleDMX = format(pAngleDMX, '016b')
tAngleDMX = format(tAngleDMX, '016b')

tAnglefine = int(tAngleDMX[8:16],2)
tAnglecoarse = int(tAngleDMX[0:8],2)

print tAnglefine
print tAnglecoarse
