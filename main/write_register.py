from pymodbus.payload import BinaryPayloadBuilder, Endian, BinaryPayloadDecoder

class ConvertNumber():

    def binary_pay_load(value):

        if (value < 0 ):

            builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
            builder.reset()
            builder.add_16bit_int(value)
            payload = builder.to_registers()

            return payload[0]
        
        if (value >= 0):

            return value