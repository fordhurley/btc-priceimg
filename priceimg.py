#!/usr/bin/env python

"""
priceimg.py

Copyright (C) 2013 Ford Hurley

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

import flask
from werkzeug.contrib.cache import SimpleCache
import Image, ImageDraw, ImageFont
import json, urllib
from StringIO import StringIO
import os.path

FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verdana.ttf')

app = flask.Flask(__name__)
cache = SimpleCache()

@app.route('/')
def home():
    """Serve the home page."""
    try:
        usd_per_btc = getUSDPerBTC()
    except:
        usd_per_btc = None
    if usd_per_btc is None:
        usd_per_btc = 'Mt Gox Error'
    else:
        usd_per_btc = '${0} / BTC'.format(usd_per_btc)
    return flask.render_template('index.html', usd_per_btc=usd_per_btc)

@app.route('/img')
@app.route('/img/<price_usd>')
@app.route('/img/<price_usd>/<color>')
def priceimg(price_usd=None, color='0'):
    """Serve the image.
    The StringIO trick is from here:
    http://stackoverflow.com/a/10170635/576932
    """
    try:
        price_usd = float(price_usd)
    except:
        return "Error: bad USD price argument"
    try:
        color = getColor(color)
    except:
        return "Error: bad color argument"

    try:
        usd_per_btc = getUSDPerBTC()
    except:
        return "Error: Mt Gox error"
    
    price_btc = price_usd / usd_per_btc
    img_io = getImageIO(price_btc, color)     

    return flask.send_file(img_io, attachment_filename='img.png')
    
@app.route('/balance/<address>')
@app.route('/balance/<address>/<color>')
def balimg(address=None, color='0'):
   #Serve image with address balance
   try:
       address = float(balance(address))
   except:
       return "Error: bad address argument"
   try:
        color = getColor(color)
   except:
        return "Error: bad color argument"
   img_io = getImageIO(address, color)
   
   return flask.send_file(img_io, attachment_filename='img.png')

def balance(address):
    """
    Check balance of an address on blockchain.info.
    <balance> should be a valid bitcoin address.
    """
    url = 'http://blockchain.info/rawaddr/' + address + '?format=json'
    urlfh = urllib.urlopen(url)
    data = json.load(urlfh)
    balance = data['final_balance']/1e8
    urlfh.close()
    
    return balance
	

def getColor(color):
    """Decode color string argument from URL

    Colors can be passed as either a full HTML code (#aac24e),
    short HTML code (#c00), or as a single hex digit for
    grayscale (#5). The '#' symbol is always optional. Case is
    ignored.

    Returns a RGB tuple (values 0-255).

    >>> getColor('#aac24e')
    (170, 194, 78)

    >>> getColor('c00')
    (204, 0, 0)

    >>> getColor('5')
    (85, 85, 85)
    """

    if color[0] == '#':
        color = color[1:]
    if len(color) == 1:
        rgb = color*2, color*2, color*2
    elif len(color) == 3:
        rgb = color[0]*2, color[1]*2, color[2]*2
    elif len(color) == 6:
        rgb = color[:2], color[2:4], color[4:]
    else:
        raise ValueError('Invalid color')

    rgb = tuple([int(c, 16) for c in rgb])
    return rgb

def getUSDPerBTC():
    """Get current exchange rate as a float.

    Caches the exchange rate for five minutes.
    """

    usd_per_btc = cache.get('usd_per_btc')

    if usd_per_btc is None:
        url = 'http://data.mtgox.com/api/1/BTCUSD/ticker'
        urlfh = urllib.urlopen(url)
        data = json.load(urlfh)
        usd_per_btc = float(data['return']['avg']['value'])
        urlfh.close()
        cache.set('usd_per_btc', usd_per_btc, timeout=300)

    return usd_per_btc

def generateImage(price_btc, color):
    """Generate an Image object.

    To try to get better looking images, the original image
    is 4x larger and it is scaled down with antialiasing.
    """

    price_str = '{0:.4f} BTC'.format(price_btc)
    w, h = int(len(price_str) * 30 + 16), 56

    img = Image.new('RGBA', (w, h), (255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(FONT_PATH, 50)
    except:
        font = ImageFont.load_default()

    draw.text((0, 0), price_str, font=font, fill=color)
    img = img.resize((w/4, h/4), Image.ANTIALIAS)

    return img

def getImageIO(price_btc, color):
    """Get the StringIO object containing the image.

    Also cached, with a name containing the BTC price and color."""

    img_name = 'img_{0:f}_{1}[0]_{1}[1]_{1}[2]'.format(price_btc, color)
    img_io = cache.get(img_name)

    if img_io is None:
        img = generateImage(price_btc, color)
        img_io = StringIO()
        img.save(img_io, 'PNG', quality=90)
        img_io.seek(0)
        cache.set(img_name, img_io, timeout=300)

    img_io.seek(0)
    return img_io

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
