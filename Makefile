version ?= latest
IMAGE = leocbs/searchlinks:$(version)

image: 
	docker build -t $(IMAGE) .

check: image
	docker run --rm $(IMAGE) python tests/parser_tests.py