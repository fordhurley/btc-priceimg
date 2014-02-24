"""
Copyright (C) 2014 Ford Hurley

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import requests
from StringIO import StringIO
import tempfile

from PIL import Image, ImageDraw, ImageFont

from priceimg import app, cache


def download_asset(url):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        r = requests.get(url)
        f.write(r.content)
        return f.name


def get_balance(address):
    """
    Check balance of an address on blockchain.info.
    <address> should be a valid bitcoin address.
    """
    url = 'http://blockchain.info/rawaddr/' + address + '?format=json'
    r = requests.get(url)
    data = r.json()
    balance = data['final_balance'] / 1e8
    return balance


def get_color(color):
    """Decode color string argument from URL

    Colors can be passed as either a full HTML code (#aac24e),
    short HTML code (#c00), or as a single hex digit for
    grayscale (#5). The '#' symbol is always optional. Case is
    ignored.

    Returns a RGB tuple (values 0-255).

    >>> get_color('#aac24e')
    (170, 194, 78)

    >>> get_color('c00')
    (204, 0, 0)

    >>> get_color('5')
    (85, 85, 85)
    """

    if color[0] == '#':
        color = color[1:]
    if len(color) == 1:
        rgb = color * 2, color * 2, color * 2
    elif len(color) == 3:
        rgb = color[0] * 2, color[1] * 2, color[2] * 2
    elif len(color) == 6:
        rgb = color[:2], color[2:4], color[4:]
    else:
        raise ValueError('Invalid color')

    rgb = tuple([int(c, 16) for c in rgb])
    return rgb


def get_usd_per_btc():
    """Get current exchange rate as a float.

    Caches the exchange rate for five minutes.
    """
    usd_per_btc = cache.get('usd_per_btc')

    if usd_per_btc is None:
        url = 'http://data.mtgox.com/api/1/BTCUSD/ticker'
        r = requests.get(url)
        data = r.json()
        usd_per_btc = float(data['return']['avg']['value'])
        cache.set('usd_per_btc', usd_per_btc, timeout=300)

    return usd_per_btc


def get_usd_per_ltc():
    """Get current exchange rate as a float.

    Caches the exchange rate for five minutes.
    """
    usd_per_ltc = cache.get('usd_per_ltc')

    if usd_per_ltc is None:
        url = 'https://btc-e.com/api/2/ltc_usd/ticker'
        r = requests.get(url)
        data = r.json()
        usd_per_ltc = float(data['ticker']['avg'])
        urlfh.close()
        cache.set('usd_per_ltc', usd_per_ltc, timeout=300)

    return usd_per_ltc


def generate_image(price, currency, color):
    """Generate an Image object.

    price is a float, and currency is a three letter string
    to be shown after the price (e.g., 'BTC').

    To try to get better looking images, the original image
    is 4x larger and it is scaled down with antialiasing.
    """

    price_str = '{0:.4f} {1}'.format(price, currency)
    w, h = int(len(price_str) * 30 + 16), 56

    img = Image.new('RGBA', (w, h), (255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(app.config['FONT_PATH'], 50)
    except:
        font = ImageFont.load_default()

    draw.text((0, 0), price_str, font=font, fill=color)
    img = img.resize((w / 4, h / 4), Image.ANTIALIAS)

    return img


def get_image_io(price, currency, color):
    """Get the StringIO object containing the image.

    Also cached, with a name containing the BTC price and color."""

    img_name = 'img_{0:f}_{1}_{2}[0]_{2}[1]_{2}[2]'.format(price, currency, color)
    img_io = cache.get(img_name)

    if img_io is None:
        img = generate_image(price, currency, color)
        img_io = StringIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        cache.set(img_name, img_io, timeout=300)

    img_io.seek(0)
    return img_io
