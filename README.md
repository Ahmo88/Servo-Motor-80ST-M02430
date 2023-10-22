# Servo-Motor-80ST-M02430

    This code project will controll "Servo-Motor-80ST-M02430" driver/servo motor
    using python GUI app and USB-RS485 for communication with Servo Driver

# Git project config
    git config --local user.name "Ahmo Tokalic"
    git config --local user.email "tarevo_1988@hotmail.com"

# Python version
    - 3.11.5    

# How to setup:
    - pip install pyModbus
    - pip install pyserial  

# Wiring RS485:
    in RS485 communication, you typically only need two wires, often referred to as "A" and "B" or sometimes "TX+" and "TX-". These two wires are used for bidirectional communication, allowing you to both send and receive data between your USB-RS485 adapter and the connected device.

    Wire "A" (TX+): This wire is used for transmitting data from your USB-RS485 adapter to the connected device.

    Wire "B" (TX-): This wire is used for receiving data from the connected device back to your USB-RS485 adapter.

    By using these two wires, you can establish two-way communication with your device. Just make sure that the adapter and the connected device are configured with the same baud rate, data bits, stop bits, and parity settings to ensure proper communication.

    However, there can be situations where connecting the grounds of both devices (USB-RS485 adapter and the connected device) may be beneficial:

    1. **Common Ground Reference:** If the USB-RS485 adapter and the connected device are powered from different sources, having a common ground reference can help stabilize the communication by ensuring that both devices are working with the same voltage reference.

    2. **Noise Reduction:** Grounding can help reduce electrical noise and interference in the communication. It can provide a stable reference point for the signals and reduce the risk of data errors, especially in environments with a lot of electrical noise.

    3. **Long Cable Runs:** In situations where you have long cable runs between the devices, having a ground connection can help maintain signal integrity over longer distances.

    While it's not always necessary, it's a good practice to include a ground connection if you encounter communication issues or if your RS485 communication spans a significant distance. However, if you're working with short cable runs in a controlled environment and you're not experiencing problems, you may not need to connect the grounds. Always refer to the specific requirements of your setup and consider consulting the documentation for your devices.

# Servo Driver Parameters setup:
    - All this can be faunded in V4.0 Servo driver Technical Manual in project
        Pn001 must be 4 if we use Servo motor CNCSERVO CONTROL "80ST-M02430"
        Pn064 must be 2 for rs485 communication, or 1 if we use rs232 communication
        Pn066 can be 2 for 19200 baudrate, remember to change in Windows and python code same baudrate!!
        Pn067 must be 6 for 8 , N , 2 ( Modbus , RTU ) communication function 
        Pn069 4095 Input function control mode select register 2   
        Pn071 4095 Input function logic state set register 2

# Shaft rotation scale:
    - Driver use register 120 and 121 for Servo shaft rotation
        register 120, full turns (if is 1 then will turn shaft 1 times "360" degre) 
        register 121, partial turns (if is 5000 it will turn shaft half "180" degre, if is 2500 then "90" degree)

    - Driver use register 387 for encoder position and it contains 2 registers registers[0] and registers[1]
        registers[1] is for hight bit (full turns)
        registers[0] is for low bit (partial turns)
                 
    So we use scale for "partial turns" registers[0]. In code if we need to print value of 0.5 then we 
    scale encoder rough value registers[0] for example 5000 * 0.0001 == 0.5 turns (half turn). 
    In this case we will se that encoder position is 0.5  

    It is same for writing 121 register, only we need to scale with 10000.
    For example in input we write "0.5 value" but in code scale (0.5 input value * 10000) so we get 5000 (180 degree == half turns)
    
    So for encoder scale register 387 is registers[0] * 0.0001, and for partial 121 scale * 10000
