import cv2
from PIL import Image

def detect_edges(path):
    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return cv2.Canny(gray, 100, 200)

def edge_embed(image, text, edge_map):
    image = image.convert("RGB")
    binary = ''.join(format(ord(c), '08b') for c in text) + '11111110'
    idx = 0
    img = image.copy()

    for y in range(img.height):
        for x in range(img.width):
            if idx >= len(binary):
                return img
            if edge_map[y][x] != 0:
                r, g, b = img.getpixel((x, y))
                if idx < len(binary):
                    r = (r & ~1) | int(binary[idx]); idx += 1
                if idx < len(binary):
                    g = (g & ~1) | int(binary[idx]); idx += 1
                if idx < len(binary):
                    b = (b & ~1) | int(binary[idx]); idx += 1
                img.putpixel((x, y), (r, g, b))
    return img

def edge_decode(image, edge_map):
    image = image.convert("RGB")
    binary = ""
    for y in range(image.height):
        for x in range(image.width):
            if edge_map[y][x] != 0:
                r, g, b = image.getpixel((x, y))
                binary += str(r & 1) + str(g & 1) + str(b & 1)
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    msg = ""
    for c in chars:
        if c == '11111110':
            break
        try:
            msg += chr(int(c, 2))
        except ValueError:
            continue
    return msg
