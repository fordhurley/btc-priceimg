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
