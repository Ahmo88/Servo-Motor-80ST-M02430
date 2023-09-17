from pymodbus.client.serial import ModbusSerialClient as ModbusClient
from connect_rs485 import RS485Connection
import time

# rtu is Modbus RTU communication mode
client = RS485Connection.connectRS485('rtu', 'COM3', 19200)

# communicate with Modbus slave ID 2 over Serial (port 0)
slave_address = 2


def servo_on():
    client.write_register(3, 1, slave_address)
    print("Servo is ON")


def servo_off():
    client.write_register(3, 0, slave_address)
    print("Servo is OFF")


def rotateShaft():

    client.write_register(128, 50, slave_address)  # set speed
    time.sleep(0.2)
    # amout of rotations (if is 1 then is 1 full turn)
    client.write_register(120, 1, slave_address)
    time.sleep(0.1)
    client.write_register(71, 4095, slave_address)
    time.sleep(0.1)
    client.write_register(71, 3071, slave_address)


def readRegister():

    try:
        # Try to establish a connection
        if client.connect():
            print("Connected to the Modbus device")

            # Specify the Modbus slave address
            slave_address = 2  # Replace with the correct slave address for your device

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

    except Exception as e:
        print("An error occurred:", str(e))


# servo_off()
servo_on()
rotateShaft()
