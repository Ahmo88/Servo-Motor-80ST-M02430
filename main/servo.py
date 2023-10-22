from logger_config import logging
from write_register import ConvertNumber

class Servo():
    """ This is main class for controlling Servo motor using USB-RS485 adapter and Modbus RTU 
        We call all methods in this class from main.py template  
        Also we use threading for loop so we can read encoder constantly
    """
   
    def __init__(self, client):

      self.client = client 
      # communicate with Modbus slave ID 2 over Serial (port 0)
      self.slave_address = 2 # Servo is slave and id is 2

    def servo_on(self):

        if self.client:
            self.client.write_register(3, 1, self.slave_address)
            logging.info("Servo is ON")
        else:
            logging.warning('USB-RS485 adapter is not connected. Please insert USB-RS485 adapter ')


    def servo_off(self):
        self.client.write_register(3, 0, self.slave_address)
        logging.info("Servo is OFF")

    def servo_speed(self, speed):
         self.client.write_register(128, speed, self.slave_address)  # set speed

    def rotate_shaft(self, full_turn, partial_turn):
        """ this method will write values from template inputs to registers
            and it will rotate servo shaft 
        """

        if self.client:
            try:

                # Pn120=12，Pn121=5000 Example: the encoder 2500 line, shaft will make 12.5 turns
                self.client.write_register(120, ConvertNumber.binary_pay_load(full_turn), self.slave_address) # full turns (if is 1 then will turn shaft 1 times "360" degre)
                self.client.write_register(121, ConvertNumber.binary_pay_load(partial_turn), self.slave_address) # partial turns (if is 5000 it will turn shaft half "180" degre, if is 2500 then "90" degree)

                self.client.write_register(71, 4095, self.slave_address)
                self.client.write_register(71, 3071, self.slave_address)


            except Exception as e:
                # Code to handle the exception
                logging.warning('Wrong input type for servo position')
                logging.warning(f"An error occurred: {e}")

        else:
            logging.warning('USB-RS485 adapter is not connected. Please insert USB-RS485 adapter ')  

    def set_torque(self):
            
            self.client.write_register(8, ConvertNumber.binary_pay_load(300), self.slave_address) # shaft torque CCW (0 to 300 max torque Newton-meters (N·m) or ounce-inches (oz·in))
            self.client.write_register(9, ConvertNumber.binary_pay_load(-300), self.slave_address) # shaft torque CW (-300 to 0 max torque Newton-meters (N·m) or ounce-inches (oz·in))    
                 