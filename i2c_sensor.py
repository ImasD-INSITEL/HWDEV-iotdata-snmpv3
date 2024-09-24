#import sys
#import board
#import busio

#i2c= busio.I2C(board.SCL,board.SDA)

#print("DISPOSITIVOS i2C ",[hex(i) for i in i2c.scan()])

#ads = 0x48

#if not ads in i2c.scan():
	#print("No encuentro el ads1115")
	#sys.exit()

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Crear el objeto I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Crear el objeto ADS
ads = ADS.ADS1115(i2c)

# Crear el objeto canal para leer (canal 0 en este caso)
chan = AnalogIn(ads, ADS.P0)

while True:
    # Leer y mostrar el valor en volts
    print("Valor:", chan.value)
    print("Volts:", chan.voltage)
    print("Volts Reales:", (chan.voltage/0.052119)-0.069)

    time.sleep(1)