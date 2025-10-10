
class HexMap:
    
    def __init__(self, input_path="image\png\screenshot.png"):
        self.input_path = input_path
        self.hex_size = 13
        pass

    def __str__(self):
        return f"Hello"







if __name__ == "__main__":
    print('This is run from OOP.py file')
    hex_map = HexMap()
    print(hex_map)
    print(hex_map.hex_size,hex_map.input_path)
    hex_map.hex_size = 50
    print(hex_map.hex_size,hex_map.input_path)

