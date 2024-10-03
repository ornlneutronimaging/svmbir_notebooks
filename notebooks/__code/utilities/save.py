from PIL import Image


def make_tiff(data=[], filename='', metadata=None):
    new_image = Image.fromarray(data)
    if metadata:
        new_image.save(filename, tiffinfo=metadata)
    else:
        new_image.save(filename)
        