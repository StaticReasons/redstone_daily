from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


def new_image(width, height):
    global base_image
    base_image = Image.new('RGB', (width, height), (255, 255, 255))


def draw_network_icon(url, x, y, width, height):
    network_icon_url = url
    response = requests.get(network_icon_url)
    network_icon = Image.open(BytesIO(response.content))
    network_icon_resized = network_icon.resize((width, height))
    base_image.paste(network_icon_resized, (x, y))


def draw(videos):
    height = 2048
    width = 1024
    new_image(width, height)
    draw = ImageDraw.Draw(base_image)

    first_video = videos.pop(0)
    draw_network_icon('https:' + first_video['cover_url'], 64, 400, 896, 504)

    base_image.show()
