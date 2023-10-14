from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from connect_rs485 import RS485Connection
import time
from logger_config import logging
from pymodbus.exceptions import ModbusIOException
from write_register import ConvertNumber

# rtu is Modbus RTU communication mode
client = RS485Connection.connectRS485('rtu', 'COM7', 19200)

# communicate with Modbus slave ID 2 over Serial (port 0)
slave_address = 2 # Servo is slave and id in manual is 2

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


    def rotate_shaft(full_turn, partial_turn):
        if client:
            client.write_register(128, 100, slave_address)  # set speed
            
            # Pn120=12，Pn121=5000 Example: the encoder 2500 line, shaft will make 12.5 turns
            client.write_register(120, ConvertNumber.binary_pay_load(full_turn), slave_address) # full turns (if is 1 then will turn shaft 1 times "360" degre)
            client.write_register(121, ConvertNumber.binary_pay_load(partial_turn), slave_address) # partial turns (if is 5000 it will turn shaft half "180" degre, if is 2500 then "90" degree)

            client.write_register(71, 4095, slave_address)
            client.write_register(71, 3071, slave_address)

        else:
            logging.warning('USB-RS485 adapter is not connected. Please insert USB-RS485 adapter ')  

    def set_torque():
            
            client.write_register(8, ConvertNumber.binary_pay_load(300), slave_address) # shaft torque CCW (0 to 300 max torque Newton-meters (N·m) or ounce-inches (oz·in))
            client.write_register(9, ConvertNumber.binary_pay_load(-300), slave_address) # shaft torque CW (-300 to 0 max torque Newton-meters (N·m) or ounce-inches (oz·in))
          

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
#servo = Servo.set_torque(self=None) 
#servo = Servo.rotate_shaft(self=None)
servo = Servo.readRegister(self=None)        
