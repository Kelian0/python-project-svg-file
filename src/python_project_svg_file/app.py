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

        for i in range(hex_per_row):
            for j in range(hex_per_col):
                if i % 2 == 1:
                    off_set = vert_spacing / 2
                else:
                    off_set = 0
                hex_mapping[i, j, 0] = int(i * horiz_spacing)
                hex_mapping[i, j, 1] = int(j * vert_spacing + off_set)
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
        for i in range(m):
            for j in range(n):
                if (
                    hex_mapping[i, j, 0] > size
                    and hex_mapping[i, j, 1] > size
                    and hex_mapping[i, j, 1] < fig.size[1] - size
                    and hex_mapping[i, j, 0] < fig.size[0] - size
                ):
                    draw_hex(fig, hex_mapping[i, j, 0], hex_mapping[i, j, 1], size)
        return None
    return (draw_hex_from_mapping,)


@app.cell
def _(draw_hex_from_mapping, image, map_hex):
    size = 13
    testing_image = image.copy()
    hex_map = map_hex(image, size)

    draw_hex_from_mapping(testing_image, hex_mapping=hex_map, size=size)

    testing_image.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
