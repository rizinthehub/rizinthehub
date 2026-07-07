from PIL import Image, ImageOps, ImageEnhance
from html import escape

IMAGE_PATH = "assets/ascii-source.png"
OUTPUT_PATH = "ascii_tspans.txt"

# Tune these if needed
WIDTH = 34
START_X = 20
START_Y = 30
LINE_HEIGHT = 20

# Dense charset, similar chaotic Andrew style
ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def resize_image(image, new_width):
    width, height = image.size
    aspect_ratio = height / width

    # 0.48 compensates for monospace characters being taller than wide
    new_height = int(aspect_ratio * new_width * 0.48)

    return image.resize((new_width, new_height))

def image_to_ascii():
    image = Image.open(IMAGE_PATH).convert("L")

    # Increase contrast so the ASCII has stronger structure
    image = ImageEnhance.Contrast(image).enhance(1.8)

    # Optional sharpen feel through autocontrast
    image = ImageOps.autocontrast(image)

    # Invert so darker image regions become denser characters
    image = ImageOps.invert(image)

    image = resize_image(image, WIDTH)

    pixels = list(image.getdata())
    chars = []

    for pixel in pixels:
        index = int(pixel / 255 * (len(ASCII_CHARS) - 1))
        chars.append(ASCII_CHARS[index])

    lines = [
        "".join(chars[i:i + WIDTH])
        for i in range(0, len(chars), WIDTH)
    ]

    tspans = []

    y = START_Y
    for line in lines:
        safe_line = escape(line)
        tspans.append(f'<tspan x="{START_X}" y="{y}">{safe_line}</tspan>')
        y += LINE_HEIGHT

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(tspans))

    print(f"Done. ASCII SVG tspans saved to {OUTPUT_PATH}")
    print(f"Lines: {len(lines)}")
    print(f"Width: {WIDTH}")

if __name__ == "__main__":
    image_to_ascii()