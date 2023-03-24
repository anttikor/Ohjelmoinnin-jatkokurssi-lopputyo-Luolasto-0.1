from PIL import Image
#import numpy as np
#from scipy.misc import imresize

def lohikaarme(skaala):
    img = Image.open("conv\lohikaarme2.jpg")
    img = img.resize((skaala, skaala))

    pixels = img.load()
    matrix = [[0 for j in range(skaala)] for i in range(skaala)]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            matrix[i][j] = (int(r), int(g), int(b))
    return matrix

    

def hero(skaala):
    img = Image.open("conv\hero2.jpg")
    img = img.resize((skaala, skaala))

    pixels = img.load()
    matrix = [[0 for j in range(skaala)] for i in range(skaala)]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            matrix[i][j] = (int(r), int(g), int(b))
    return matrix

def stone(skaala):
    img = Image.open("conv\stone.jpg")
    img = img.resize((skaala, skaala))

    pixels = img.load()
    matrix = [[0 for j in range(skaala)] for i in range(skaala)]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            matrix[i][j] = (int(r), int(g), int(b))
    return matrix

def dirt_road(skaala):
    img = Image.open("conv\dirt_road3.jpg")
    img = img.resize((skaala, skaala))

    pixels = img.load()
    matrix = [[0 for j in range(skaala)] for i in range(skaala)]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            matrix[i][j] = (int(r), int(g), int(b))
    return matrix

def piirtaja(skaala):
    matriisi = [[0 for j in range(skaala)] for i in range(skaala)]

def resize_image(matrix, skaala):
    img = Image.new("RGB", (250, 250), "white")
    pixels = img.load()
    for i in range(250):
        for j in range(250):
            r, g, b = matrix[i][j]
            pixels[i, j] = (r, g, b)

    img = img.resize((skaala, skaala))
    pixels = img.load()
    new_matrix = [[0 for j in range(skaala)] for i in range(skaala)]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            new_matrix[i][j] = (int(r), int(g), int(b))
    return new_matrix

"""
def resize_image_numpylla(matrix, skaala):
    img = np.array(matrix, dtype=np.uint8)
    img = imresize(img, (skaala, skaala), interp='bilinear')
    return img.tolist()
"""


