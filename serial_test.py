#!/usr/bin/env python3
import serial
import time

expected_message_size = 4

def read_buffer(ser):
    messages = []
    lines_read = 0
    while ser.in_waiting >= expected_message_size:
        line = ser.readline()
        
        # if line doesn't end with EOL character DUMP IT IN THE TRASH!!!!
        if '\\n'in str(line): 
            messages.append(line.decode('utf-8').rstrip())
            lines_read += 1
            print(f"lines read: {lines_read}")
        else: 
            print(f"Bad line: {str(line)}")

    return messages

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.reset_input_buffer()

    send_interval = 2
    last_send = 0

    while True:
        messages = read_buffer(ser)

        for message in messages:
            print(message)
        
        if time.time() >= last_send + send_interval:
            print("sending message...")
            last_send = time.time()
            ser.write("123".encode('utf-8'))