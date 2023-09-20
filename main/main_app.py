from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from connect_rs485 import RS485Connection
import time
from logger_config import logging

# rtu is Modbus RTU communication mode
client = RS485Connection.connectRS485('rtu', 'COM3', 19200)

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


    def readRegister(self):

        # Read holding registers
        response = client.read_holding_registers(
            address=387, count=2, unit=slave_address)

        if response.isError():
            print("Modbus error:", response)
        else:
            # Get the data from the response
            register_values = response.registers
            low_byte = register_values[0]
            high_byte = register_values[1]

            # Combine low and high bytes to form a 16-bit value
            value = (high_byte << 8) | low_byte
            print("Register Value:", value)


        # servo_off()
        self.servo_on()
        self.rotateShaft()
        # readRegister()
        
#servo = Servo.servo_off(self=None)        
