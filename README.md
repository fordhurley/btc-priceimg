# Bitcoin Price Image Generator

The bitcoin price image generator is a simple tool that creates a dynamic image of a
price in BTC, based on a fixed USD price. The resulting image can be embedded in a
forum post, for example, and it will always show an up-to-date BTC equivalent price.
This is useful when you want to show a price for something in BTC, but you want the
price to be pinned to a USD value (and not have to update your post every day as the
BTC/USD exchange rate fluctuates). This tool relies on the
[global weighted average](https://bitcoinaverage.com/explain.htm) from
[BitcoinAverage](https://bitcoinaverage.com).

Problems? Suggestions? [Open an issue](https://github.com/fordhurley/btc-priceimg/issues).

Source available on [GitHub](https://github.com/fordhurley/btc-priceimg).

The advanced version of the tool allows for a choice of currency (BTC or LTC for now).
Read about it [below](#advanced).


## Usage

Simply build a URL of the form:

    http://btc-priceimg.herokuapp.com/img/<price_in_usd>

Where `<price_in_usd>` is the price you want in USD.

You can also add an optional color argument to change the color of the text:

    http://btc-priceimg.herokuapp.com/img/<price_in_usd>/<color>

The color code should be an html-like hex code (for white: `ffffff` or `fff` or
simply `f`). See <a href="https://en.wikipedia.org/wiki/Web_colors" target="_blank">wikipedia</a>
for more info. The background of the image will be transparent.


## Example

Say you want to sell an item for $10. You can generate an image using:

    http://btc-priceimg.herokuapp.com/img/10.00


Which will yield the image: <img src="http://btc-priceimg.herokuapp.com/img/10.00"/>

If you want to change the color (to more closely match the text in your forum post,
for example), use:

    http://btc-priceimg.herokuapp.com/img/10.00/00f

Which yields: <img src="http://btc-priceimg.herokuapp.com/img/10.00/00f"/>

You can then embed the image in your post using that URL. In BBCode, this would
be:

    [img]http://btc-priceimg.herokuapp.com/img/10.00[/img]


## Advanced Version

The advanced version is available to allow changing the display currency, and allow
for fancier options in the future. The URL format is of the form:

    http://btc-priceimg.herokuapp.com/advimg?price=<price>&currency=<currency>&color=<color>

Arguments:

- `price` the desired price in USD (required)
- `currency` should be "BTC" or "LTC" (without quotes). Defaults to "BTC".
- `color` same as in the basic version above.

Example:

    http://btc-priceimg.herokuapp.com/advimg?price=10+USD&currency=BTC&color=f00

<img src="http://btc-priceimg.herokuapp.com/advimg?price=10+USD&currency=BTC&color=f00">


## Balance Checker

An additional tool allows you to check the balance of any bitcoin address using the
API from <a href="http://blockchain.info" target="_blank">blockchain.info</a>.
Simply build a URL of the form:

    http://btc-priceimg.herokuapp.com/balance/<address>/<color>

As in the basic version above, the color argument is optional and accepts html-like hex codes.

Example:

    http://btc-priceimg.herokuapp.com/balance/122LV3CNADj1yHU2tFPEhcCWR5QbfMzNcm

<img src="http://btc-priceimg.herokuapp.com/balance/122LV3CNADj1yHU2tFPEhcCWR5QbfMzNcm">


by <a href="http://fordhurley.com">Ford Hurley</a>
(<a href="bitcoin:122LV3CNADj1yHU2tFPEhcCWR5QbfMzNcm?label=btc-priceimg">122LV3CNADj1yHU2tFPEhcCWR5QbfMzNcm</a>)
