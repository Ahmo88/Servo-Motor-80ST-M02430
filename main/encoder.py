

#NOTE MAIN PROBLEM HERE IS IF WE USE THREADING WE CANNOT USE control_servo_template.py script
# IF WE DON'T RUN THIS SCRIPT THEN WE CAN USE control_servo_template.py script
# I HAVE TO FIND WEY TO RUN BOTH WITHOUT PROBLEMS

import time
from logger_config import logging
from pymodbus.exceptions import ModbusIOException
import threading  
from main_app import Servo
from connect_rs485 import RS485Connection

def read_encoder_registers():

    client = RS485Connection.connectRS485('rtu', 'COM7', 19200)
    slave_address = 2

    try:
        while True:  # Keep reading the registers continuously
            # Read the holding registers starting from address 387, for a count of 2 registers
            result = client.read_holding_registers(387, 2, slave_address)

            # Check if the request was successful
            if result.isError():
                print(f"Failed to read the registers: {result}")
            else:
                # Get the data from the response
                j = result.registers[0]  # low bit
                i = result.registers[1]  # high bit
                print("Low bit:", j)
                print("High bit:", i)

            # Adjust the time interval based on your needs
            time.sleep(0.2)  # Read every 1 second
    except ModbusIOException as e:
        print(f"Modbus communication error: {e}")

# Start the reading process in a separate thread
read_thread = threading.Thread(target=read_encoder_registers)
read_thread.daemon = True  # Allow the thread to exit when the main program exits
read_thread.start()

while True:
    pass