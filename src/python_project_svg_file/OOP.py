from PIL import Image, ImageDraw
import numpy as np

class HexTransform:
    
    def __init__(self, input_path="image\png\screenshot.png"):
        self.input_path = input_path
        self.input_image = Image.open("image\png\screenshot.png")
        self.xmax = self.input_image.size[0]
        self.ymax = self.input_image.size[1]
        self.img_ratio = self.xmax/self.ymax
        self.input_maping = None
        self.input_hex_size = None
        pass

    def __str__(self):
        return f"Hello"

    def map(self, hex_per_col):
        
        vert_spacing = self.ymax / (hex_per_col + 0.5)
        off_set = 0.5 * vert_spacing
        hex_size = vert_spacing /(np.sqrt(3))
        self.input_hex_size = hex_size
        horiz_spacing = 3 / 2 * hex_size

        hex_per_row = int(self.xmax // horiz_spacing) + 1 

        if self.xmax % horiz_spacing >= (1/3) * horiz_spacing:
            hex_per_row += 1


        hex_mapping = np.empty((hex_per_col,hex_per_row, 2))

        for i in range(hex_per_col):
            for j in range(hex_per_row):
                if j % 2 == 1:
                    off_set = vert_spacing / 2
                else:
                    off_set = 0

                hex_mapping[i, j, 0] = j * horiz_spacing
                hex_mapping[i, j, 1] = i * vert_spacing + off_set

        self.input_maping = hex_mapping

        return hex_mapping
    
    def show_mapping(self):
        m, n = self.input_maping.shape[0], self.input_maping.shape[1]
        image = self.input_image.copy()
        draw = ImageDraw.Draw(image)
        for j in range(m):
            for i in range(n):
                if (
                    self.input_maping[j, i, 0] > self.input_hex_size
                    and self.input_maping[j, i, 1] > self.input_hex_size
                    and self.input_maping[j, i, 0] < self.xmax - self.input_hex_size
                    and self.input_maping[j, i, 1] < self.ymax - self.input_hex_size
                ):
                    draw.circle((self.input_maping[j, i, 0], self.input_maping[j, i, 1]), radius=self.input_hex_size, outline=(0, 255, 0, 0))
        image.show()

    def build_svg(self,output_path):
        pass





if __name__ == "__main__":
    # print('This is run from OOP.py file')
    hex_map = HexTransform()
    print(hex_map)
    hex_map.map(22)
    hex_map.show_mapping()