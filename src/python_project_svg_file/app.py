import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from PIL import Image
    return Image, mo, np


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
        horiz_spacing = 3 / 2 * size
        vert_spacing = np.sqrt(3) * size

        hex_per_row = int(img.size[0] // horiz_spacing)
        hex_per_col = int(img.size[1] // vert_spacing)

        hex_mapping = np.empty((hex_per_row, hex_per_col, 2))

        for i in range(hex_per_row):
            for j in range(hex_per_col):
                if j % 2 == 1:
                    off_set = size
                else:
                    off_set = 0
                hex_mapping[i, j, 0] = int(i * vert_spacing)
                hex_mapping[i, j, 1] = int(j * horiz_spacing + off_set)
        # GREEN = (0, 255, 0, 0)
        # draw = ImageDraw.Draw(img)
        # draw.circle((),outline=GREEN)

        return hex_mapping
    return (map_hex,)


@app.cell
def _(image, map_hex):
    hex_map = map_hex(image, 50)

    print(hex_map)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
