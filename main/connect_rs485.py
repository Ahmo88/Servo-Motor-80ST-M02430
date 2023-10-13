# NOTE: Code is not tested yet it is just sample from gptchat i have to check and continue.
from pymodbus.client.serial import ModbusSerialClient as ModbusClient


class RS485Connection():
    def __init__(self) -> None:
        pass

    def connectRS485(method: str, port: str, baudrate: int):

        try:
            # Create a Modbus client
            client = ModbusClient(method=method, port=port,
                                  stopbits=2, bytesize=8, parity='N', baudrate=baudrate)

            # Try to establish a connection
            if client.connect():
                print("Connected to the Modbus device")
                return client

            else:
                print("Failed to connect to the Modbus device")

        except Exception as e:
            print("An error occurred:", str(e))
