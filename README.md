# Scrapy Trial

## Requirements

- Linux
- Python 3.5+
- Virtualenv

## Installation

Run the following commands in the terminal to create a virtual environment and pip install requirements:
```sh
make env && make install
```

## Usage

To run the spider:
```sh
make run
```

To test the spider:
```sh
make test
```

To check the source code lint (PEP8):
```sh
make lint
```

To deploy the spider in Scrapy Cloud:
```sh
. .env/bin/activate
pip install shub
shub login
shub deploy
```

## Scrapinghub Cloud Job
See spider job status in [Scrapinghub Cloud]((https://app.scrapinghub.com/p/342867/1)) (Preview: `scrapinghub-cloud-job.png`).


## Author

- Fernando Felix do Nascimento Junior
