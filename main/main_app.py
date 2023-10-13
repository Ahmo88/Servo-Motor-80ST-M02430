from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from connect_rs485 import RS485Connection
import time
from logger_config import logging
from pymodbus.exceptions import ModbusIOException

# rtu is Modbus RTU communication mode
client = RS485Connection.connectRS485('rtu', 'COM7', 19200)

# communicate with Modbus slave ID 2 over Serial (port 0)
slave_address = 2

class Servo():
    """ This is main class for controlling Servo motor using USB-RS485 adapter and Modbus RTU """
    def __init__(self, name, age):
      self.name = name
      self.age = age

    def servo_on(self):
        if client:
            client.write_register(3, 1, slave_address)
            logging.info("Servo is ON")
        else:
            logging.warning('USB-RS485 adapter is not connected. Please insert USB-RS485 adapter ')


    def servo_off(self):
        client.write_register(3, 0, slave_address)
        logging.info("Servo is OFF")


    def rotateShaft(self):

        if client:
            client.write_register(128, 50, slave_address)  # set speed
            time.sleep(0.2)
            # amout of rotations (if is 1 then is 1 full turn)
            client.write_register(120, 1, slave_address)
            time.sleep(0.1)
            client.write_register(71, 4095, slave_address)
            time.sleep(0.1)
            client.write_register(71, 3071, slave_address)
        else:
            logging.warning('USB-RS485 adapter is not connected. Please insert USB-RS485 adapter ')    

    # NOTE: JUST TEST
    time.sleep(1)
    rotateShaft(self=None)

    def readRegister(self):

        try:
            # Read the holding registers starting from address 387, for a count of 2 registers
            result = client.read_holding_registers(387, 2, slave_address)  # Replace 'unit' with your device's unit ID

            # Check if the request was successful
            if result.isError():
                print(f"Failed to read the registers: {result}")
            else:
                # Get the data from the response
                j = result.registers[0]  # low bit
                i = result.registers[1]  # high bit
                print("Low bit:", j)
                print("High bit:", i)
        except ModbusIOException as e:
            print(f"Modbus communication error: {e}")
  
        
servo = Servo.servo_on(self=None) 

servo = Servo.readRegister(self=None)        
