from PIL import Image, ImageDraw
import numpy as np
from python_project_svg_file.Sampling_strategy import circle_filter

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

    def avg_px(self, x0, y0):
        x_lim = self.xmax
        y_lim = self.ymax
        nb_px = 0
        avg_color = np.zeros(3)
        filter = circle_filter
        mask_x,mask_y = filter.mask(filter,x=x0,y=y0,radius=self.input_hex_size)
        for i in range(len(mask_x)):
                x = x0 + mask_x[i]
                y = y0 + mask_y[i]
                if (x > 0 and x < x_lim) and (y > 0 and y < y_lim):
                    avg_color += np.array(self.input_image.getpixel((x, y)))
                    nb_px += 1
        return avg_color / nb_px

    def build_svg(self,output_path):
        pass





if __name__ == "__main__":
    # print('This is run from OOP.py file')
    hex_map = HexTransform()
    print(hex_map)
    hex_map.map(22)
    print(hex_map.avg_px(0,0))