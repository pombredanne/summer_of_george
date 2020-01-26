import re


class KeyArrayToRegex():

    mapper = None

    def __init__(self, mapper):
        self.mapper = mapper

    def transform_to_array(self, keys):
        return [ self.mapper.transform(key) for key in keys ]

    def transform(self, keys):
        return ''.join(self.transform_to_array(keys))

    def transform_and_compress(self, keys):
        compressed_expression = ''
        number_of_keys = len(keys)
        if number_of_keys == 0:
            return compressed_expression

        apply_plus = 1
        transformed_array = self.transform_to_array(keys)
        prev_ = transformed_array[0]

        for index in range(1, number_of_keys):
            item = transformed_array[index]
            if prev_ == item:
                apply_plus += 1
                continue

            compressed_expression += prev_
            if apply_plus > 1:
                compressed_expression += '{' + str(apply_plus) + '}'

            prev_ = item
            apply_plus = 1

        compressed_expression += prev_
        if apply_plus:
            compressed_expression += '+'

        return compressed_expression
