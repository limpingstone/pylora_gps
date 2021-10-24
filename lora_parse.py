
def str_to_byte(input_str):
    byte_str = []
    for char in list(input_str):
        byte_str.append(ord(char))

    return byte_str

def byte_to_str(input_byte):
    output_str = ""
    for byte in byte_str: 
        output_str += chr(byte)

    return output_str

