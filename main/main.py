# NOTE: Code is not tested yet it is just sample from gptchat i have to check and continue.

from pymodbus.client.serial import ModbusSerialClient


# Configure the Modbus RTU client
client = ModbusSerialClient(
    #method='rtu', port='/dev/ttyUSB0', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1 # for linux
    method='rtu', port='COM1', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1  # connection method for windows
)

# Connect to the RS485 port
if not client.connect():
    print("Failed to connect to the RS485 port")
    exit()

# Function to turn the servo on
def servo_on():
    try:
        # Write single registers to turn on the servo
        client.write_registers(33, [1], unit=2)
        client.write_registers(34, [4], unit=2)
        client.write_registers(35, [2], unit=2)
        client.write_registers(3, [1], unit=2)
        client.write_registers(40, [10000], unit=2)
        client.write_registers(41, [10000], unit=2)
        print("Servo turned on")
    except Exception as e:
        print(f"Error turning on servo: {str(e)}")

# Function to turn the servo off
def servo_off():
    try:
        # Write single registers to turn off the servo
        client.write_registers(3, [0], unit=2)
        print("Servo turned off")
    except Exception as e:
        print(f"Error turning off servo: {str(e)}")

# Call the functions to control the servo
servo_on()
# You can add a delay or other code here if needed
servo_off()

# Close the Modbus connection
client.close()
