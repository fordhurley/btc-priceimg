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
import subprocess
import re

from priceimg import app, cache


def download_asset(url, extension=''):
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as f:
        r = requests.get(url)
        r.raise_for_status()
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


price_regex = re.compile(r'([0-9]*\.?[0-9]+)\s*(\w+)?')

def parse_price(s):
    """Parses a price string of the form "1.5 USD".

    >>> parse_price('1.5 USD')
    (1.5, 'USD')

    >>> parse_price('1')
    (1.0, 'USD')

    >>> parse_price('0.1USD')
    (0.1, 'USD')

    >>> parse_price('1 GBP')
    (1.0, 'GBP')
    """
    s = s.strip()
    m = price_regex.match(s)
    price, currency = m.groups()
    price = float(price)
    if currency is None:
        currency = 'USD'
    return price, currency


def parse_color(color):
    """Decode color string argument from URL

    Colors can be passed as either a full HTML code (#aac24e),
    short HTML code (#c00), or as a single hex digit for
    grayscale (#5). The '#' symbol is always optional. Case is
    ignored.

    Returns a RGB tuple (values 0-255).

    >>> parse_color('#aac24e')
    (170, 194, 78)

    >>> parse_color('c00')
    (204, 0, 0)

    >>> parse_color('5')
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


def get_exchange_rate(input_currency, output_currency):
    """Gets the exchange rate as output_currency per input_currency.

    Caches the result for five minutes.
    """
    input_currency = input_currency.lower()
    output_currency = output_currency.lower()
    key = '%s_per_%s' % (output_currency, input_currency)
    rate = cache.get(key)
    if rate is None:
        if output_currency == 'btc':
            rate = get_btc_rate(input_currency)
        elif output_currency == 'ltc' and input_currency == 'usd':
            rate = get_ltc_per_usd()
        else:
            raise ValueError('unsupported currency pair')
        cache.set(key, rate, timeout=300)
        # TODO: cache the inverse while we have it?
    return rate


def get_btc_rate(currency):
    currency = currency.upper()
    url = 'https://apiv2.bitcoinaverage.com/indices/global/ticker/BTC%s' % currency
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    per_btc = float(data['averages']['day'])
    return 1.0 / per_btc


def get_ltc_per_usd():
    url = 'https://btc-e.com/api/2/ltc_usd/ticker'
    r = requests.get(url)
    data = r.json()
    usd_per_ltc = float(data['ticker']['avg'])
    return 1.0 / usd_per_ltc


def generate_image(price, currency, color):
    """Generate an Image object.

    price is a float, and currency is a three letter string
    to be shown after the price (e.g., 'BTC').

    To try to get better looking images, the original image
    is 4x larger and it is scaled down with antialiasing.
    """

    price_str = '{0:.4f} {1}'.format(price, currency)
    w = int(len(price_str) * 30 + 16)
    h = 30

    cmd = ['convert']

    cmd.append('-size')
    cmd.append('%dx%d' % (w, h))

    cmd.append('xc:none')

    cmd.append('-font')
    cmd.append(app.config['FONT_PATH'])

    cmd.append('-pointsize')
    cmd.append('14')

    cmd.append('-gravity')
    cmd.append('center')

    cmd.append('-fill')
    cmd.append('rgb(%d,%d,%d)' % color)

    cmd.append('-draw')
    cmd.append('text 0,0 "%s"' % price_str)

    cmd.append('-trim')
    cmd.append('+repage')

    cmd.append('png:-')

    img = subprocess.check_output(cmd)

    return img


def get_image_io(price, currency, color):
    """Get the StringIO object containing the image.

    Also cached, with a name containing the BTC price and color."""

    img_name = 'img_{0:f}_{1}_{2}[0]_{2}[1]_{2}[2]'.format(price, currency, color)
    img_io = cache.get(img_name)

    if img_io is None:
        img = generate_image(price, currency, color)
        img_io = StringIO()
        img_io.write(img)
        img_io.seek(0)
        cache.set(img_name, img_io, timeout=300)

    img_io.seek(0)
    return img_io
