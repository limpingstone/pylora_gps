#!/usr/bin/python3
from MTK33X9 import MTK33X9
from lora import LoRa
import lora_parse
import time

def print_gps_info(current_data):
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



def main(): 
    mtk33x9 = MTK33X9()
    mtk33x9.ser_init('/dev/serial0')

    lora = LoRa()

    try: 
        while (True):
            current_data = mtk33x9.get_current_data()
            if (current_data.is_complete()):
                #print_gps_info(current_data)

                buff = "%02d:%02d:%02d.%03d,%2d %.4f %c,%03d %.4f %c, %.2f" % (
                    current_data.hour, 
                    current_data.minute, 
                    current_data.second, 
                    current_data.msec,
                    current_data.lat_deg, 
                    current_data.lat_min, 
                    current_data.lat_pos,
                    current_data.long_deg, 
                    current_data.long_min, 
                    current_data.long_pos,
                    current_data.speed
                )

                print(buff)
                len_padding = 256 - len(buff)
                buff = buff.ljust(len_padding, ' ')

                lora.write_fifo(lora_parse.str_to_byte(buff), 0)
                lora.transmit()
    
            time.sleep(0.1)
    except KeyboardInterrupt: 
        mtk33x9.ser_stop()

if __name__ == "__main__":
    main()

