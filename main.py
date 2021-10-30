#!/usr/bin/python3
from MTK33X9 import MTK33X9
from MTK33X9 import MTK33X9_data
from lora import LoRa
from calc_prediction import Prediction
import RPi.GPIO as GPIO
import lora_parse
import time
import sys


# define dev_path and dev_name in config.py
import config

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


def lora_send_data(lora, current_data):
    buff = ">>>>%s:%02d%02d%02d.%03d,%2d%.4f,%c,%03d%.4f,%c,%.2f>" % (
            config.dev_name,
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

    # Construct packet sent
    print("Tx sending: " + buff)
    len_padding = 256 - len(buff)
    buff = buff.ljust(len_padding, ' ')

    lora.write_fifo(lora_parse.str_to_byte(buff), 0)
    lora.transmit()


def lora_receive_data(lora):
    if (not lora.listen()):
        raise TimeoutError()
        return None
    else:
        buff = lora.read_fifo()
        #print("Rx received: " + lora_parse.byte_to_str(buff)[1:80])
        buff = lora_parse.byte_to_str(buff[1:80])

        return lora_parse.str_to_data(buff)


def main(): 
    mtk33x9 = MTK33X9()
    mtk33x9.ser_init(config.dev_path)

    lora = LoRa()

    rx_data = MTK33X9_data()

    try: 
        while (True):
            current_data = mtk33x9.get_current_data()
            if (current_data.is_complete()):
                lora_send_data(lora, current_data)

                #print('Sent GPS information...')
                print('Sent GPS information: ')
                print_gps_info(current_data)

            time.sleep(0.1)

            try: 
                incoming_data = lora_receive_data(lora)
                if (incoming_data.is_complete()):
                    rx_data = incoming_data
                    #print('Received GPS information...')
                    print('Received GPS information: ')
                    print_gps_info(rx_data)
                    
            except TimeoutError:
                print('Timeout reached!')
            except IndexError:
                print('Current data received not valid!') 
            
            time.sleep(0.1)

            if (current_data.is_complete() and rx_data.is_complete()):
                print('-------------------------------')
                current_prediction = Prediction(current_data, rx_data)
                print("Real time data: " + str(current_prediction.is_realtime))

            print('===============================================')
            print()

    except KeyboardInterrupt: 
        mtk33x9.ser_stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()

