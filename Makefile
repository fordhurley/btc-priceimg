IMAGE := fordhurley/btc-priceimg:latest

PHONY: image, serve, test

image:
	docker build --tag ${IMAGE} .

serve: image
	docker run --rm -p 5002:5002 -v ${PWD}:/app ${IMAGE}

test: image
	docker run --rm -e FLASK_ENV=test ${IMAGE} nosetests -v
