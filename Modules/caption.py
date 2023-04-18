from PIL import Image, ImageDraw, ImageFont
import pathlib
import uuid
import wget

def caption_this(image_url, text, text_position, font_size, color=None): 
    img_path = pathlib.Path(wget.download(image_url, out="Images/Stellaris"))
    return add_text_to_image(img_path, text, text_position, font_size)
    
def add_text_to_image(image, text, position, font_size, padding=10):
    # Open the image
    img = Image.open(image)

    # Create an ImageDraw object
    draw = ImageDraw.Draw(img)

    # Set the font and font size
    font = ImageFont.truetype("resources/Arial_Bold.ttf", font_size)

    # Get the size of the text
    text_size = draw.textsize(text, font=font)

    # Calculate the coordinates for the text
    if position == 'top':
        x = (img.width - text_size[0]) / 2
        y = padding
    elif position == 'bottom':
        x = (img.width - text_size[0]) / 2
        y = img.height - text_size[1] - padding
    else:
        raise ValueError("Invalid value for 'position': {}".format(position))
    
    # Get the current color palette of the image
    palette = img.getpalette()

    # Add white (255, 255, 255) as the first color in the palette
    if len(palette) > 255:
        palette = palette[:-1]
    
    palette = [255, 255, 255] + palette

    # Set the new palette for the image
    img.putpalette(palette)

    # Draw the text on the image
    draw.text((x, y), text, font=font, fill=palette[0])
    
    # Save the modified image
    path = "Media/Caption" + str(uuid.uuid4()) + ".png"    
    img.save(path)
    
    return path


def get_color(image):
    # Open the image
    img = Image.open(image)
    
    # Get the color palette of the image
    palette = img.getpalette()

    # Calculate the distance between each color in the palette and white
    # in the RGB color space
    distances = []
    for i in range(0, len(palette), 3):
        r, g, b = palette[i:i+3]
        distance = (r - 255)**2 + (g - 255)**2 + (b - 255)**2
        distances.append(distance)

    # Find the index of the color in the palette with the smallest distance to white
    closest_color_index = distances.index(min(distances))

    # Get the RGB values of the closest color
    closest_color = palette[closest_color_index*3:closest_color_index*3+3]

    # Print the closest color
    print(closest_color)
    return closest_color