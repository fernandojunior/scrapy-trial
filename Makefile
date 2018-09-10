.PHONY: clean
 
help:
	@echo 'Usage: make [command]'
	@echo 'Commands:'
	@echo '  env          Create a virtual development environment for Python.'
	@echo '  install      Install dependencies into virtualenv.'
	@echo '  lint         Check code style with flake8.'
	@echo '  test         Run tests quickly with pytest.'
	@echo '  build        Build a distribution package with setuptools.'
	@echo '  clean        Remove all Python, test and build artifacts.'
	@echo '  clean-build  Remove build artifacts.'
	@echo '  clean-pyc    Remove Python file artifacts.'
	@echo '  clean-test   Remove test artifacts.'

build:
	python setup.py egg_info sdist bdist_wheel
	ls -l dist

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .pytest_cache/

env:
	sudo apt-get -y install python3-pip
	sudo pip3 install virtualenv
	virtualenv .env

install:
	test -f requirements.txt && \
		. .env/bin/activate && pip install -r requirements.txt \
		|| echo "requirements.txt doesn't exists"

lint:
	. .env/bin/activate && flake8 --show-source --count

test:
	. .env/bin/activate && py.test

run:
	test -f arts.json && rm arts.json || echo "arts.json doesn't exists"
	. .env/bin/activate && scrapy runspider src/spider.py -o arts.json
