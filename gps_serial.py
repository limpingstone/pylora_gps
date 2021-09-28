import serial

print('Starting serial at 9600 baud...')
ser = serial.Serial(
    port='/dev/serial0', \
    baudrate=9600)

print('Updating serial configuration to 115200 baud...')
ser.write(b'$PMTK251,115200*1F\r\n')

ser.close()
ser = serial.Serial(
    port='/dev/serial0', \
    baudrate=115200)

print('Updating NMEA frequency and fix CTL to 5 Hz...')
ser.write(b'$PMTK220,200*2C\r\n')
ser.write(b'$PMTK300,200,0,0,0,0*2F\r\n')

def parse_time(time_str): 
    if len(time_str) != 10:
        raise ValueError('Invalid time string!')

    hour   = int(time_str[0:2])
    minute = int(time_str[2:4])
    second = int(time_str[4:6])
    msec   = int(time_str[7:10])
    print("%02d:%02d:%02d.%03d UTC" % (hour, minute, second, msec))

try: 
    while True:
        line = ser.readline()
        line_pos = line.decode('ASCII').split(',')
        if line_pos[0] == '$GPGGA':
            parse_time(line_pos[1])
            for pos in line_pos:
                print(pos)

except KeyboardInterrupt:
    print('\nClosing serial connection...')
    ser.close()
    print('Exited!')

