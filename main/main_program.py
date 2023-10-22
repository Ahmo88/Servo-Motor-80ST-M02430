import tkinter as tk
from tkinter import ttk
from servo import Servo
from logger_config import logging
from connect_rs485 import RS485Connection
import threading # is for separate thread, so we can run code separate from main code. This prevent conflict
# for example if we need run some loop separate from this program, so main program can be used withot interference  
from pymodbus.exceptions import ModbusIOException
import time


class Client():
    def __init__(self) -> None:
       self.client = RS485Connection.connectRS485('rtu', 'COM7', 19200)
       self.slave_address = 2


class MainProgram():
     def __init__(self) -> None:
         self.client =  Client()
     
     def run_program():
        """ This is main program, template azure. when program start Servo template will run"""

        def read_encoder_registers():
            """ method read encoder register/ encoder position and send to template field """

            try:       
                
                # Read the holding registers starting from address 387, for a count of 2 registers
                result = rs485Client.client.read_holding_registers(387, 2, rs485Client.slave_address)

                # Check if the request was successful
                if result.isError():
                    print(f"Failed to read the registers: {result}")
                else:
                    # Get the data from the response/result (encoder)
                    i = result.registers[1]  # high bit (for example 1 is 1 full turn == 360 deg)
                    j = result.registers[0]  # low bit (for examplee 5000 is 0.5 half turn == 180 deg)

                    fb_position_entry.delete(0, tk.END)  # Clear the current value
                    fb_position_entry.insert(0, str(i + j*0.0001))  # j*0.0001 *(convert for example 5000 * 0.0001 == 0.5, it is half turn )
                    return i + j

            except ModbusIOException as e:
                print(f"Modbus communication error: {e}")            

        def _read_encoder_continuously():
            """ loop for reading encoder """
            
            while True:

                read_encoder_registers()
                time.sleep(0.1)


        def start_reading_encoder():
                """ method called from main.py template
                    it will start Thread, and read encoder           
                """
                # This method will start a separate thread to read the encoder registers continuously
                encoder_thread = threading.Thread(target=_read_encoder_continuously)
                encoder_thread.daemon = True
                encoder_thread.start() 
        

        root = tk.Tk()
        root.title('Servo controlling template')

        window_height = 530
        window_width = 800

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        style = ttk.Style(root)
        root.tk.call('source', r'C:\Users\tarev\OneDrive\Asiakirjat\GitHub\Servo-Motor-80ST-M02430\main\azure dark.tcl')
        style.theme_use('azure')


        g = tk.IntVar()
        g.set(75)
        h = tk.IntVar()

        frame1 = ttk.LabelFrame(root, text='Just a frame', width=210, height=200)
        frame1.place(x=20, y=12)

        fb_position = ttk.Label(root, text="feedback position:")
        fb_position.place(x=20, y=240)
        fb_position_entry = ttk.Entry(root)
        fb_position_entry.place(x=20, y=260)
        fb_position_entry.insert(0, "0")
        
 
        # Input fields, for full and partial turns
        label = ttk.Label(root, text="Full turn:")
        label.place(x=250, y=20)
        input_position_entry = ttk.Entry(root)
        input_position_entry.place(x=250, y=40)
        input_position_entry.insert(0, '0')


        label3 = ttk.Label(root, text="Speed: 0~3000 r/min")
        label3.place(x=250, y=160)
        servo_speed_entry = ttk.Entry(root)
        servo_speed_entry.place(x=250, y=180)
        servo_speed_entry.insert(0, '300')

        rs485Client = Client()
        servo = Servo(rs485Client.client)

        button_set_speed = ttk.Button(root, text='Set Speed', 
                            command=lambda: servo.servo_speed(speed = int(servo_speed_entry.get())))
        button_set_speed.place(x=250, y=220)

        """ spin = ttk.Spinbox(root, from_=0, to=100, increment=0.1)
        spin.place(x=250, y=70)
        spin.insert(0, 'Spinbox') """


        def split_values():
            
            # TODO: # TRY TO ORGANIZE THIS FILE AND ADD COMMENTS TO ALL METHODS

            global full_turns  # Use the global keyword to work with the outer-scope variable
            global partial_turns  # Use the global keyword to work with the outer-scope variable

            if (0.1 <= float(input_position_entry.get()) <= 0.9) or (-0.9 <= float(input_position_entry.get()) <= -0.1):
                full_turns = 0
                partial_turns = float(input_position_entry.get())
                partial_turns = int(partial_turns * 10000)


            else:
                
                number_str = str(input_position_entry.get())
                full_turns, partial_turns = number_str.split('.')
                full_turns = int(full_turns)

                if "-" in str(full_turns):                   
                    partial_turns = int(partial_turns)
                    partial_turns = -partial_turns * 1000

                else:               
                    partial_turns = int(partial_turns)
                    partial_turns = partial_turns * 1000    

        button_rotate_shaft = ttk.Button(root, text='Rotate shaft', 
            command=lambda: (
                split_values(),
                servo.rotate_shaft(full_turn=full_turns, partial_turn= int(partial_turns))
                  # Call your second method here
            )
        )
                                    
        button_rotate_shaft.place(x=250, y=320)


        def scale(i):
            g.set(int(scale.get()))

        scale = ttk.Scale(root, from_=100, to=0, variable=g, command=scale)
        scale.place(x=80, y=430)

        progress = ttk.Progressbar(root, value=0, variable=g, mode='determinate')
        progress.place(x=80, y=480)

        def toggle_switch():
            """ this method will turn on/off Servo motor """
            if h.get() == 1:
                servo.servo_on()  # Call function when switch is ON
                switch.config(text='Servo ON')  # Update the text when the switch is ON
            else:
                servo.servo_off()  # Call function when switch is OFF
                switch.config(text='Servo OFF')  # Update the text when the switch is ON
                
        switch = ttk.Checkbutton(root, text='Servo state', style='Switch', variable=h, offvalue=0, onvalue=1, command=toggle_switch)
        switch.place(x=250, y=470)

        size = ttk.Sizegrip(root)
        size.place(x=780, y=510)

        sep1 = ttk.Separator()
        sep1.place(x=20, y=235, width=210)


        def method_to_run_after_frame_load():
            position = start_reading_encoder()

        # Execute the method after the window frame loads
        root.after(0, method_to_run_after_frame_load())

        root.mainloop()

if __name__ == "__main__":

    MainProgram.run_program()
