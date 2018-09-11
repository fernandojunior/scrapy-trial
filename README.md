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
pip install shub
shub login
shub deploy <your_project_id_here>
```

## Author

- Fernando Felix do Nascimento Junior
