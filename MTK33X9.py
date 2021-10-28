import serial
import threading

class MTK33X9_data: 
    def __init__(self):
        self.debug_mode  = False
        self.hour        = None
        self.minute      = None
        self.second      = None
        self.msec        = None
        self.lat_pos     = None
        self.lat_deg     = None
        self.lat_min     = None
        self.long_pos    = None
        self.long_deg    = None
        self.long_min    = None
        self.speed       = None

    def parse_time(self, time_str): 
        if (len(time_str) != 10):
            raise ValueError('Invalid time string!')
    
        self.hour   = int(time_str[0:2])
        self.minute = int(time_str[2:4])
        self.second = int(time_str[4:6])
        self.msec   = int(time_str[7:10])

        if (self.debug_mode):
            print("%02d:%02d:%02d.%03d UTC" % (self.hour, self.minute, self.second, self.msec))
    
    def parse_latitude(self, lat_str, lat_pos):
        if (len(lat_str) != 9):
            raise ValueError('Invalid latitude string!')
        elif (lat_pos != 'N' and lat_pos != 'S'):
            raise ValueError('Invalid latitude orientation!')
    
        self.lat_pos = lat_pos
        self.lat_deg = int  (lat_str[0:2])
        self.lat_min = float(lat_str[2:9])

        if (self.debug_mode):
            print("%3d deg %.4f' %c" % (self.lat_deg, self.lat_min, self.lat_pos))
    
    def parse_longitude(self, long_str, long_pos):
        if (len(long_str) != 10):
            raise ValueError('Invalid longitude string!')
        elif (long_pos != 'E' and long_pos != 'W'):
            raise ValueError('Invalid longitude orientation!')
    
        self.long_pos = long_pos
        self.long_deg = int  (long_str[0:3])
        self.long_min = float(long_str[3:10])

        if (self.debug_mode):
            print("%3d deg %.4f' %c" % (self.long_deg, self.long_min, self.long_pos))
    
    def parse_speed_km(self, speed_str, speed_unit):
        #if (len(speed_str) != 5):
        #    raise ValueError('Invalid speed string!')
        if (speed_unit != 'K'):
            raise ValueError('Invalid speed unit!')

        self.speed = float(speed_str)
    
        if (self.debug_mode):
            print("%.2f km/h" % self.speed)

    def is_complete(self):
        return ((self.hour is not None) and  
                (self.minute   is not None) and  
                (self.second   is not None) and 
                (self.msec     is not None) and 
                (self.lat_pos  is not None) and  
                (self.lat_deg  is not None) and 
                (self.lat_min  is not None) and 
                (self.long_pos is not None) and 
                (self.long_deg is not None) and 
                (self.long_min is not None) and 
                (self.speed    is not None))
    

class MTK33X9_thread(threading.Thread):
    def __init__(self, dev_path):
        threading.Thread.__init__(self)
        self.dev_path     = dev_path
        self.current_data = MTK33X9_data()

    def ser_init(self):
        print('Starting serial at 9600 baud...')
        self.ser = serial.Serial(
            port     = self.dev_path, \
            baudrate = 9600)
        
        print('Updating serial configuration to 115200 baud...')
        self.ser.write(b'$PMTK251,115200*1F\r\n')
        
        # Reinitialize serial at 115200 baud
        self.ser.close()
        self.ser = serial.Serial(
            port     = self.dev_path, \
            baudrate = 115200)
        
        print('Updating NMEA frequency and fix CTL to 5 Hz...')
        self.ser.write(b'$PMTK220,200*2C\r\n')
        self.ser.write(b'$PMTK300,200,0,0,0,0*2F\r\n')

    def ser_stop(self):
        if (self.ser.isOpen()):
            print('\nClosing serial connection...')
            self.ser.close()

    def run(self):
        current_data = MTK33X9_data()
        while (self.kbd_interrupt == False):
            line = self.ser.readline()

            try:
                line_pos = line.decode('ASCII').split(',')
                if (line_pos[0] == '$GPGGA' or line_pos[0] == '$GNGGA'):
                    current_data.parse_time     (line_pos[1])
                    current_data.parse_latitude (line_pos[2], line_pos[3][0])
                    current_data.parse_longitude(line_pos[4], line_pos[5][0])
        
                elif (line_pos[0] == '$GPVTG' or line_pos[0] == '$GNVTG'):
                    current_data.parse_speed_km(line_pos[7], line_pos[8])
    
                if (current_data.is_complete()):  
                    self.current_data = current_data 
            except UnicodeDecodeError:
                print('Skipped line!')

    def get_current_data(self):
        return self.current_data

class MTK33X9:
    def ser_init(self, dev_path):
        # Initialize parameters 
        self.thread = MTK33X9_thread(dev_path)
        self.thread.daemon = True

        # While loop flag for keyboard interrupt
        self.thread.kbd_interrupt = False

        # Open serial connection and start polling
        self.thread.ser_init()
        self.thread.start()

    def ser_stop(self):
        # Signal while loop to stop
        self.thread.kbd_interrupt = True

        # Stop polling and close serial connection
        self.thread.join()
        self.thread.ser_stop()
        print('Exited!')

    def get_current_data(self):
        return self.thread.get_current_data()

