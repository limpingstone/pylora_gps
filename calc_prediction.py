#!/usr/bin/python3
from datetime import datetime

class Prediction: 
    def __init__(self, local_data, received_data):
        self.is_realtime   = False
        self.local_data    = local_data
        self.received_data = received_data
        self.calc_realtime()

        pass

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

