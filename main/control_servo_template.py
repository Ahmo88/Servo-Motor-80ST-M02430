import tkinter as tk
from tkinter import ttk
from main_app import Servo
from logger_config import logging
from connect_rs485 import RS485Connection

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


# Input fields, for full and partial turns
# Create a label for the entry
label = ttk.Label(root, text="Full turn:")
label.place(x=250, y=20)
full_turn_entry = ttk.Entry(root)
full_turn_entry.place(x=250, y=40)
full_turn_entry.insert(0, '0')

label2 = ttk.Label(root, text="Partial turn:")
label2.place(x=250, y=80)
partial_turn_entry = ttk.Entry(root)
partial_turn_entry.place(x=250, y=100)
partial_turn_entry.insert(0, '0')

label3 = ttk.Label(root, text="Speed: 0~3000 r/min")
label3.place(x=250, y=160)
servo_speed_entry = ttk.Entry(root)
servo_speed_entry.place(x=250, y=180)
servo_speed_entry.insert(0, '300')

client = RS485Connection.connectRS485('rtu', 'COM7', 19200)
servo = Servo(client)

button_set_speed = ttk.Button(root, text='Set Speed', 
                    command=lambda: servo.servo_speed(speed = int(servo_speed_entry.get())))
button_set_speed.place(x=250, y=220)

""" spin = ttk.Spinbox(root, from_=0, to=100, increment=0.1)
spin.place(x=250, y=70)
spin.insert(0, 'Spinbox') """


# Rotate Sertvo shaft
button_rotate_shaft = ttk.Button(root, text='Rotate shaft', 
                    command=lambda: servo.rotate_shaft(full_turn = int(full_turn_entry.get()), 
                                                       partial_turn = int(partial_turn_entry.get())))
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

root.mainloop()
