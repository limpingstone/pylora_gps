import serial
import threading

class MTK33X9_thread(threading.Thread):
    def __init__(self, dev_path):
        threading.Thread.__init__(self)

        print('Starting serial at 9600 baud...')
        self.ser = serial.Serial(
            port     = dev_path, \
            baudrate = 9600)
        
        print('Updating serial configuration to 115200 baud...')
        self.ser.write(b'$PMTK251,115200*1F\r\n')
        
        self.ser.close()
        self.ser = serial.Serial(
            port     = dev_path, \
            baudrate = 115200)
        
        print('Updating NMEA frequency and fix CTL to 5 Hz...')
        self.ser.write(b'$PMTK220,200*2C\r\n')
        self.ser.write(b'$PMTK300,200,0,0,0,0*2F\r\n')

        while (True):
            line = self.ser.readline()

            line_pos = line.decode('ASCII').split(',')
            for pos in line_pos:
                print(pos)

    def __del__(self):
        if (self.ser.isOpen()):
            print('\nClosing serial connection...')
            self.ser.close()

    def run(self):
        while (True):
            line = self.ser.readline()

            line_pos = line.decode('ASCII').split(',')
            for pos in line_pos:
                print(pos)


class MTK33X9:
    def __init__(self, dev_path): 
        self.thread = MTK33X9_thread(dev_path)
        self.thread.start()

