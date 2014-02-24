from flask import send_file, request, render_template

from priceimg import app
import util

@app.route('/')
def home():
    """Serve the home page."""
    try:
        usd_per_btc = util.get_usd_per_btc()
    except:
        usd_per_btc = None
    if usd_per_btc is None:
        usd_per_btc = 'Mt Gox Error'
    else:
        usd_per_btc = '${0} / BTC'.format(usd_per_btc)
    try:
        usd_per_ltc = util.get_usd_per_ltc()
    except:
        usd_per_ltc = None
    if usd_per_ltc is None:
        usd_per_ltc = 'BTC-e Error'
    else:
        usd_per_ltc = '${0} / LTC'.format(usd_per_ltc)

    return render_template('index.html', usd_per_btc=usd_per_btc, usd_per_ltc=usd_per_ltc)


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
    except ValueError:
        return "Error: bad USD price argument"

    try:
        color = util.get_color(color)
    except ValueError:
        return "Error: bad color argument"

    try:
        usd_per_btc = util.get_usd_per_btc()
    except Exception:
        return "Error: Mt Gox error"

    price_btc = price_usd / usd_per_btc

    img_io = util.get_image_io(price_btc, 'BTC', color)

    return send_file(img_io, attachment_filename='img.png')


@app.route('/advimg')
def priceimgadv():
    """Serve the image, with advanced options.

    The StringIO trick is from here:
    http://stackoverflow.com/a/10170635/576932
    """
    price_usd = request.args.get('price')
    currency = request.args.get('currency', 'BTC').upper()
    color = request.args.get('color', '0')

    try:
        price_usd = float(price_usd)
    except:
        return "Error: bad USD price argument"

    try:
        color = util.get_color(color)
    except:
        return "Error: bad color argument"

    if currency == 'BTC':
        try:
            usd_per_coin = util.get_usd_per_btc()
        except:
            return "Error: Mt Gox error"
    elif currency == 'LTC':
        try:
            usd_per_coin = util.get_usd_per_ltc()
        except:
            return 'Error: BTC-e error'
    else:
        return 'Error: unsupported currency: ' + currency

    price = price_usd / usd_per_coin

    img_io = util.get_image_io(price, currency, color)

    return send_file(img_io, attachment_filename='img.png')


@app.route('/balance')
@app.route('/balance/<address>')
@app.route('/balance/<address>/<color>')
def balimg(address=None, color='0'):
    """Serve image with address balance."""
    try:
        address = float(util.get_balance(address))
    except:
        return "Error: bad address argument"
    try:
        color = util.get_color(color)
    except:
        return "Error: bad color argument"
    img_io = util.get_image_io(address, 'BTC', color)

    return send_file(img_io, attachment_filename='img.png')
