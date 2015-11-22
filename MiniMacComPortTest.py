import pysimpledmx
COMport = "/dev/cu.usbserial-ENYXTLPV"
mydmx = pysimpledmx.DMXConnection(COMport)

mydmx.setChannel(2, 0)
mydmx.setChannel(6, 0)
mydmx.setChannel(7, 0)
mydmx.render()
