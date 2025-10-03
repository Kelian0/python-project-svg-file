import marimo

__generated_with = "0.16.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from PIL import Image
    return (Image,)


@app.cell
def _(Image):
    image = Image.open("image\png\screenshot.png")
    # image.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
