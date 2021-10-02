#!/usr/bin/python3
from MTK33X9 import MTK33X9
import time

def main(): 
    mtk33x9 = MTK33X9()
    mtk33x9.ser_init('/dev/serial0')

    try: 
        while (True):
            current_data = mtk33x9.get_current_data()
            if (current_data.is_complete()):
                print("%02d:%02d:%02d.%03d UTC" % (
                    current_data.hour, 
                    current_data.minute, 
                    current_data.second, 
                    current_data.msec
                    )
                )
        
                print("%3d deg %.4f' %c" % (
                    current_data.lat_deg, 
                    current_data.lat_min, 
                    current_data.lat_pos
                    )
                )
        
                print("%3d deg %.4f' %c" % (
                    current_data.long_deg, 
                    current_data.long_min, 
                    current_data.long_pos
                    )
                )
        
                print("%.2f km/h" % current_data.speed)
                print()
    
            time.sleep(0.3)
    except KeyboardInterrupt: 
        mtk33x9.ser_stop()

if __name__ == "__main__":
    main()
