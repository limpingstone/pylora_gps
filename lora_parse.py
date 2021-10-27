#!/usr/bin/python3
from MTK33X9 import MTK33X9_data

def str_to_byte(input_str):
    byte_str = []
    for char in list(input_str):
        byte_str.append(ord(char))

    return byte_str

def byte_to_str(input_byte):
    output_str = ""
    for byte in input_byte: 
        output_str += chr(byte)

    return output_str

def str_to_data(rx_str):
    rx_data = MTK33X9_data() 

    # Remove extra '>' padding
    rx_str_arr = rx_str.split('>')

    # Detect for garbled data
    if len(rx_str_arr) < 3:
        return None

    rx_str = rx_str_arr[len(rx_str_arr) - 2]

    # Extract device name from received string
    rx_str_arr = rx_str.split(':')
    device_info = rx_str_arr[0]
    print("Device name: " + device_info)

    # Extract received GPS data 
    rx_str = rx_str_arr[1]
    rx_str_arr = rx_str.split(',')

    rx_data.parse_time     (rx_str_arr[0])
    rx_data.parse_latitude (rx_str_arr[1], rx_str_arr[2])
    rx_data.parse_longitude(rx_str_arr[3], rx_str_arr[4])
    rx_data.parse_speed_km (rx_str_arr[5], 'K')

    return rx_data


