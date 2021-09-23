import serial

print('starting serial at 9600 baud...')
ser = serial.Serial(
    port='/dev/serial0', \
    baudrate=9600)

print('updating serial configuration to 115200 baud...')
ser.write(b'$PMTK251,115200*1F\r\n')

ser.close()
ser = serial.Serial(
    port='/dev/serial0', \
    baudrate=115200)

print('updating NMEA frequency and fix CTL to 5 Hz...')
ser.write(b'$PMTK220,200*2C\r\n')
ser.write(b'$PMTK300,200,0,0,0,0*2F\r\n')


while True:
    line = ser.readline()
    print(line)

ser.close()

