# Servo-Motor-80ST-M02430

    This code project will controll "Servo-Motor-80ST-M02430" driver/servo motor
    using python GUI app and USB-RS485 for communication with Servo Driver

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