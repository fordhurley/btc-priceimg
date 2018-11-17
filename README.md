# btc-priceimg

https://btc-priceimg.herokuapp.com/

For help using the online tool, see USAGE.md.

## Developing

1. Install [Docker](https://docs.docker.com/engine/installation/).
2. In the cloned repo directory, run `make serve` to start the application.
3. Open http://0.0.0.0:5002/ in your browser. Note that the images in the index
file will be pulled from the production server, so you'll need to access the
images directly that you want to test. For example, http://0.0.0.0:5002/img/10.
4. Run `make test` to run the (very limited) automated tests.

### Example images for testing:

http://0.0.0.0:5002/img/10
http://0.0.0.0:5002/img/100/fff
http://0.0.0.0:5002/img/1000/ff00ff

http://0.0.0.0:5002/img@2x/50/00f

http://0.0.0.0:5002/advimg?price=10USD&currency=BTC&color=f00&dpr=1x
http://0.0.0.0:5002/advimg?price=20EUR&currency=LTC&color=ff0&dpr=1x
http://0.0.0.0:5002/advimg?price=20GBP&currency=ETH&color=0ff&dpr=2x

http://0.0.0.0:5002/balance/1E765eZrLQnhANCmgBSu3Hy2DbZktEFQ7h
http://0.0.0.0:5002/balance/1E765eZrLQnhANCmgBSu3Hy2DbZktEFQ7h/f
http://0.0.0.0:5002/balance/1E765eZrLQnhANCmgBSu3Hy2DbZktEFQ7h/ff0
