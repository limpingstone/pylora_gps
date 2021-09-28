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

def parse_latitude(lat_str, lat_pos):
    if len(lat_str) != 9:
        raise ValueError('Invalid latitude string!')
    elif lat_pos != 'N' and lat_pos != 'S':
        raise ValueError('Invalid latitude orientation!')

    lat_deg = int  (lat_str[0:2])
    lat_min = float(lat_str[2:9])
    print("%3d deg %.4f' %c" % (lat_deg, lat_min, lat_pos))

def parse_longitude(long_str, long_pos):
    if len(long_str) != 10:
        raise ValueError('Invalid longitude string!')
    elif long_pos != 'E' and long_pos != 'W':
        raise ValueError('Invalid longitude orientation!')

    long_deg = int  (long_str[0:3])
    long_min = float(long_str[3:10])
    print("%3d deg %.4f' %c" % (long_deg, long_min, long_pos))

def parse_speed_km(speed_str, speed_unit):
    #if len(speed_str) != 5:
    #    raise ValueError('Invalid speed string!')
    if speed_unit != 'K':
        raise ValueError('Invalid speed unit!')

    print("%.2f km/h" % float(speed_str))

try: 
    while True:
        line = ser.readline()

        # Need to catch UnicodeDecodeError
        line_pos = line.decode('ASCII').split(',')
        if line_pos[0] == '$GPGGA':
            parse_time     (line_pos[1])
            parse_latitude (line_pos[2], line_pos[3][0])
            parse_longitude(line_pos[4], line_pos[5][0])

        elif line_pos[0] == '$GPVTG':
            parse_speed_km(line_pos[7], line_pos[8])

except KeyboardInterrupt:
    print('\nClosing serial connection...')
    ser.close()
    print('Exited!')

