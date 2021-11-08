#!/usr/bin/python3
import math

from datetime import datetime

class Prediction: 
    def __init__(self, local_data, received_data):
        self.is_realtime   = False
        self.local_data    = local_data
        self.received_data = received_data
        self.distance      = None
        self.calc_realtime()
        self.calc_distance()

    def calc_realtime(self):
        time_format   = "%H:%M:%S.%f"
        local_time    = str(self.local_data.hour     ) + ":" \
                      + str(self.local_data.minute   ) + ":" \
                      + str(self.local_data.second   ) + "." \
                      + str(self.local_data.msec     ) + "000"

        received_time = str(self.received_data.hour  ) + ":" \
                      + str(self.received_data.minute) + ":" \
                      + str(self.received_data.second) + "." \
                      + str(self.received_data.msec  ) + "000"

        time_diff = datetime.strptime(local_time,    time_format) \
                  - datetime.strptime(received_time, time_format)

        if (abs(time_diff.total_seconds()) < 0.4):
            self.is_realtime = True

    def calc_distance(self): 
        local_lat     = self.local_data.lat_deg     + self.local_data.lat_min     / 60
        local_long    = self.local_data.long_deg    + self.local_data.long_min    / 60
        received_lat  = self.received_data.lat_deg  + self.received_data.lat_min  / 60
        received_long = self.received_data.long_deg + self.received_data.long_min / 60

        local_lat_rad     = local_lat     * math.pi / 180
        local_long_rad    = local_long    * math.pi / 180
        received_lat_rad  = received_lat  * math.pi / 180
        received_long_rad = received_long * math.pi / 180

        dlat  = received_lat_rad  - local_lat_rad
        dlong = received_long_rad - local_long_rad

        rad_km = pow(math.sin(dlat / 2), 2) + math.cos(local_lat) * math.cos(received_lat) * pow(math.sin(dlong / 2), 2);

        self.distance = 6371000 * 2 * math.asin(math.sqrt(rad_km))






