import re


class IntegerToBinaryString():
    
    expected_output_length = -1
    
    def __init__(self, expected_output_length = None):
        if not ( expected_output_length is None ):
            self.expected_output_length = int(expected_output_length)
    
    def transform(self, integer):
        binary_string = '{0:b}'.format(integer)
        if self.expected_output_length <= -1:
            return binary_string
        
        padding = '0' * self.expected_output_length
        return ( padding + binary_string )[-self.expected_output_length:]
