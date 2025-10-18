from PIL import Image, ImageDraw
import numpy as np
from python_project_svg_file.Sampling_strategy import circle_filter
import matplotlib.pyplot as plt

class HexTransform:

    def __init__(self, input_path="image\png\screenshot.png", input_hex_size=13):
        self.input_path = input_path
        self.input_image = Image.open(self.input_path)
        self.xmax = self.input_image.size[0]
        self.ymax = self.input_image.size[1]
        self.img_ratio = self.xmax/self.ymax
        self.input_hex_size = input_hex_size
        self.input_mapping = self.map(self.input_hex_size, self.xmax, self.ymax)
        self.color_map = None
        self.out_size = None
        self.output_hex_size = input_hex_size
        self.filter = circle_filter()
        pass

    def __str__(self):
        return f"Hello"

    def map(self, hex_size, xmax, ymax):
        
        vert_spacing = hex_size *(np.sqrt(3))
        hex_size = vert_spacing /(np.sqrt(3))
        horiz_spacing = 3 / 2 * hex_size

        hex_per_col = int(ymax // vert_spacing) + 1
        hex_per_row = int(xmax // horiz_spacing) + 1

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

        return hex_mapping


    def show_mapping(self):
        m, n = self.input_mapping.shape[0], self.input_mapping.shape[1]
        image = self.input_image.copy()
        draw = ImageDraw.Draw(image)
        for j in range(m):
            for i in range(n):
                draw.circle((self.input_mapping[j, i, 0], self.input_mapping[j, i, 1]), radius=self.input_hex_size, outline=(0, 255, 0, 0))
        image.show()


    def _hex_points(self,x, y,xmax,ymax):
        size = self.output_hex_size * 1.01
        i = np.array(range(6))
        angle_deg = 60 * i
        angle_rad = np.pi / 180 * angle_deg
        points = np.empty((6, 2))
        points[:, 0] = x + size * np.cos(angle_rad)
        points[:, 1] = y + size * np.sin(angle_rad)
        points[:, 0] = np.where(points[:, 0] > 0, points[:, 0], 0)
        points[:, 0] = np.where(
            points[:, 0] < xmax, points[:, 0], xmax
        )
        points[:, 1] = np.where(points[:, 1] > 0, points[:, 1], 0)
        points[:, 1] = np.where(
            points[:, 1] < ymax, points[:, 1], ymax
        )
        return np.round(points, 3)


    def _avg_px(self, x0, y0):
        nb_px = 0
        avg_color = np.zeros(3)
        filter = self.filter
        mask_x,mask_y = filter.mask(radius=self.input_hex_size*.4)
        for i in range(len(mask_x)):
            x = x0 + mask_x[i]
            y = y0 + mask_y[i]
            if (x >= 0 and x < self.xmax) and (y >= 0 and y < self.ymax):
                avg_color += np.array(self.input_image.getpixel((x, y)))
                nb_px += 1
    
        if nb_px !=0:
            return avg_color / nb_px
        else : 
            return [0,0,0]

    def color_mapping(self):
        m,n = self.input_mapping.shape[:2]
        self.color_map = np.empty((m,n,3))
        for i in range(m):
            for j in range(n):
                self.color_map[i,j] = self._avg_px(self.input_mapping[i,j,0],self.input_mapping[i,j,1])

        return self.color_map
    
    def show_color_sampling(self):
        m,n = self.input_mapping.shape[:2]
        image = self.input_image.copy()
        draw = ImageDraw.Draw(image)
        filter = self.filter
        mask_x,mask_y = filter.mask(radius=self.input_hex_size)
        for i in range(m):
            for j in range(n):
                x0 = self.input_mapping[i,j,0]
                y0 = self.input_mapping[i,j,1]
                for k in range(len(mask_x)):
                    x = x0 + mask_x[k]
                    y = y0 + mask_y[k]
                    draw.point((x,y))
        image.show()

    def build_svg(self,output_path,out_size):
        self.out_size = out_size

        self.output_ratio = out_size / self.ymax 
        
        self.output_hex_size = self.input_hex_size * self.output_ratio


        hex_map_svg = self.map(self.output_hex_size, self.out_size*self.img_ratio, self.out_size)

        hex_color_svg = self.color_mapping()

        m, n = hex_map_svg.shape[:2]

        with open(output_path, "w") as f:
            f.write(
                f"<svg height='{self.out_size}' width = '{self.out_size*self.img_ratio}' xmlns='http://www.w3.org/2000/svg'> "
            )
            f.write("\n")
            for i in range(m):
                for j in range(n):
                    x = hex_map_svg[i,j,0]
                    y = hex_map_svg[i,j,1]
                    points = self._hex_points(x,y,self.out_size*self.img_ratio,self.out_size)
                    str_points = ""
                    for point in points:
                        str_points = (str_points + str(point[0]) + "," + str(point[1]) + " ")
                    
                    str_rgb =(str(int(hex_color_svg[i, j, 0])) + " " + str(int(hex_color_svg[i, j, 1])) + " " + str(int(hex_color_svg[i, j, 2])))
                    string = ('\t<polygon points="'+ str_points + '" fill="rgb(' + str_rgb+ ')"/>')
                    f.write(string)
                    f.write("\n")
            f.write("</svg>")
        pass





if __name__ == "__main__":
    print('This is run from OOP.py file')
    hex_map = HexTransform(input_hex_size = 13)
    hex_map.build_svg(".\image\svg\out.svg",1440)

