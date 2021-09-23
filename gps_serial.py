import serial

ser = serial.Serial(
    port='/dev/serial0', \
    baudrate=9600)

while True:
    line = ser.readline()
    print(line.decode('ASCII'), end='')

ser.close()

