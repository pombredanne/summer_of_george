class StringToMapping():
    
    mapping = {}
    
    def __init__(self, mapping):
        self.mapping = mapping
        
    def transform(self, key):
        return self.mapping[key]

    def transform_array(self, array_of_keys):
        return [ self.transform(key) for key in array_of_keys ]
