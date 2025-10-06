import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from PIL import Image, ImageDraw
    return Image, ImageDraw, mo, np


@app.cell
def _(Image):
    image = Image.open("image\png\screenshot.png")
    # image.show()
    return (image,)


@app.cell
def _(image):
    print(image)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can see that the hexagones in the image are flat-top oriented""")
    return


@app.cell
def _(np):
    def map_hex(img, size):
        """
        I choose the convention odd-q
        """
        horiz_spacing = 3 / 2 * size
        vert_spacing = np.sqrt(3) * size

        hex_per_row = int(img.size[0] // horiz_spacing)
        hex_per_col = int(img.size[1] // vert_spacing)
        hex_mapping = np.empty((hex_per_row, hex_per_col, 2))

        for j in range(hex_per_row):
            for i in range(hex_per_col):
                if j % 2 == 1:
                    off_set = vert_spacing / 2
                else:
                    off_set = 0
                hex_mapping[j, i, 0] = int(j * horiz_spacing)
                hex_mapping[j, i, 1] = int(i * vert_spacing + off_set)
        # GREEN = (0, 255, 0, 0)
        # draw = ImageDraw.Draw(img)
        # draw.circle((),outline=GREEN)

        return hex_mapping
    return (map_hex,)


@app.cell
def _(ImageDraw):
    def draw_hex(fig, x, y, size):
        draw = ImageDraw.Draw(fig)
        GREEN = (0, 255, 0, 0)
        draw.circle((x, y), radius=size, outline=GREEN)
        return None


    def draw_hex_from_mapping(fig, hex_mapping, size):
        m, n = hex_mapping.shape[0], hex_mapping.shape[1]
        for j in range(m):
            for i in range(n):
                if (
                    hex_mapping[j, i, 0] > size
                    and hex_mapping[j, i, 1] > size
                    and hex_mapping[j, i, 1] < fig.size[1] - size
                    and hex_mapping[j, i, 0] < fig.size[0] - size
                ):
                    draw_hex(fig, hex_mapping[j, i, 0], hex_mapping[j, i, 1], size)
        return None
    return (draw_hex_from_mapping,)


@app.cell
def _(draw_hex_from_mapping, image, map_hex):
    size = 13
    testing_image = image.copy()
    hex_map = map_hex(image, size)

    draw_hex_from_mapping(testing_image, hex_mapping=hex_map, size=size)

    testing_image.show()
    return (hex_map,)


@app.cell
def _(np):
    def avg_px(img, x0, y0):
        x_lim = img.size[0]
        y_lim = img.size[1]
        nb_px = 0
        avg_color = np.zeros(3)
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                x = x0 + i
                y = y0 + j
                if x > 0 and x < x_lim and y > 0 and y < y_lim:
                    avg_color += np.array(img.getpixel((x, y)))
                    nb_px += 1

        return avg_color / nb_px


    def hex_color_map(img, hex_map):
        m, n = hex_map.shape[0], hex_map.shape[1]
        hex_color_map = np.empty((m, n, 3))

        x_max = img.size[0]
        y_max = img.size[1]

        for j in range(m):
            for i in range(n):
                hex_color_map[j, i] = avg_px(
                    img, hex_map[j, i, 0], hex_map[j, i, 1]
                )

        return hex_color_map
    return (hex_color_map,)


@app.cell
def _(hex_color_map, hex_map, image):
    testing_image2 = image.copy()

    hex_color = hex_color_map(testing_image2, hex_map=hex_map)
    return


@app.cell
def _(np):
    def hex_point(x, y, size, imagesizex, imagesizey):
        i = np.array(range(6))
        angle_deg = 60 * i
        angle_rad = np.pi / 180 * angle_deg
        points = np.empty((6, 2))
        points[:, 0] = x + size * np.cos(angle_rad)
        points[:, 1] = y + size * np.sin(angle_rad)
        points[:, 0] = np.where(points[:, 0] > 0, points[:, 0], 0)
        points[:, 0] = np.where(
            points[:, 0] < imagesizex, points[:, 0], imagesizex
        )
        points[:, 1] = np.where(points[:, 1] > 0, points[:, 1], 0)
        points[:, 1] = np.where(
            points[:, 1] < imagesizey, points[:, 1], imagesizey
        )
        return np.intc(points)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
