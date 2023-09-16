# NOTE: Code is not tested yet it is just sample from gptchat i have to check and continue.
import serial
from pymodbus.client.serial import ModbusSerialClient as ModbusClient

from connect_rs485 import RS485Connection

client = RS485Connection.connectRS485('rtu', 'COM3', 9600)

def servo_on():
    # Implement your Modbus write operations here
    client.write_register(33, 1)
    # delay(100) NOTE: CHECK DO WE NEED  time.sleap 100ms
    client.write_register(34, 4)
    # delay(100) NOTE: CHECK DO WE NEED  time.sleap 100ms
    client.write_register(35, 2)
    # delay(100) NOTE: CHECK DO WE NEED  time.sleap 100ms
    client.write_register(3, 1)
    # delay(100) NOTE: CHECK DO WE NEED  time.sleap 100ms
    client.write_register(40, 10000)
    # delay(100) NOTE: CHECK DO WE NEED  time.sleap 100ms
    client.write_register(41, 10000)
    # delay(100) NOTE: CHECK DO WE NEED  time.sleap 100ms

# Function to turn off the servo

def servo_off():
    # Implement your Modbus write operations here
    client.write_register(3, 0)

    pass

# Test the servo control functions
servo_on()
# Add delay or other operations here if needed

# servo_off() #turn of servo

# Close the Modbus client and serial port when done
#client.close()

