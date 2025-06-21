from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

def lsb_encode(img, text):
    img = img.convert("RGB")
    binary = text_to_bin(text) + '11111110'
    data_index = 0
    img_copy = img.copy()
    pixels = img_copy.load()

    for y in range(img_copy.height):
        for x in range(img_copy.width):
            if data_index >= len(binary):
                return img_copy
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(binary[data_index]); data_index += 1
            if data_index < len(binary):
                g = (g & ~1) | int(binary[data_index]); data_index += 1
            if data_index < len(binary):
                b = (b & ~1) | int(binary[data_index]); data_index += 1
            pixels[x, y] = (r, g, b)
    return img_copy

def lsb_decode(img):
    img = img.convert("RGB")
    pixels = img.load()
    binary = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary += str(r & 1)
            binary += str(g & 1)
            binary += str(b & 1)
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ""
    for c in chars:
        if c == '11111110':
            break
        try:
            message += chr(int(c, 2))
        except ValueError:
            continue
    return message
