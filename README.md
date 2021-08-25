# Page-loader

## Badges
[![Maintainability](https://api.codeclimate.com/v1/badges/fa73fdf8738429e795c7/maintainability)](https://codeclimate.com/github/sound-round/python-project-lvl3/maintainability)
[![Github Actions Status](https://github.com/sound-round/python-project-lvl3/actions/workflows/linter.yml/badge.svg)](https://github.com/sound-round/python-project-lvl3/actions)
[![Github Actions Status](https://github.com/sound-round/python-project-lvl3/actions/workflows/tests.yml/badge.svg)](https://github.com/sound-round/python-project-lvl3/actions)
[![Test Coverage](https://api.codeclimate.com/v1/badges/fa73fdf8738429e795c7/test_coverage)](https://codeclimate.com/github/sound-round/python-project-lvl3/test_coverage)

### Hexlet tests and linter status:
[![Actions Status](https://github.com/sound-round/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/sound-round/python-project-lvl3/actions)

## Description
Page-loader - the CLI-utility for downloading internet pages and all local resources.

## Visuals
### Downloading html
[![asciicast](https://asciinema.org/a/9Vieuv3tL6zmtohjFoKTssNfK.svg)](https://asciinema.org/a/9Vieuv3tL6zmtohjFoKTssNfK)

### Downloading images
[![asciicast](https://asciinema.org/a/9PYrmzalXG032sJYOkR9CnGV0.svg)](https://asciinema.org/a/9PYrmzalXG032sJYOkR9CnGV0)

### Downloading all resources
[![asciicast](https://asciinema.org/a/NVEhbbWInl2Puysd8AoVXJiD9.svg)](https://asciinema.org/a/NVEhbbWInl2Puysd8AoVXJiD9)

### Logging errors
[![asciicast](https://asciinema.org/a/mDkcfjAMc6sj8COhq9xfBkl6q.svg)](https://asciinema.org/a/mDkcfjAMc6sj8COhq9xfBkl6q)

### Loading bar
[![asciicast](https://asciinema.org/a/a2q0NLN5Y89kxuhRtYlo4GKTK.svg)](https://asciinema.org/a/a2q0NLN5Y89kxuhRtYlo4GKTK)

## Install
Use the following commands to install page-loader:
```
make build
make package-install
make install
```

## Local testing
Use the following command to test the package:
```
make lint
make test
```

## Usage
```
$ page-loader -h
usage: page-loader [-h] [-V] [-o OUTPUT] url

Download the page

positional arguments:
  url                   url of the page

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         output the version number
  -o OUTPUT, --output OUTPUT
                        set output folder (default: "/app")
```
## Support
If you have questions you can email me to yudaev1@gmail.com

## Links
This project was built using these tools:

| Tool                                                                        | Description                                             |
|-----------------------------------------------------------------------------|---------------------------------------------------------|
| [poetry](https://poetry.eustace.io/)                                        | "Python dependency management and packaging made easy"  |
| [flake8](https://flake8.pycqa.org/en/latest/)                               | "The tool for style guide enforcement"                  |
| [code climate](https://codeclimate.com/)                                    | "Actionable metrics for engineering"                    |
| [github actions](https://github.com/features/actions)                       | "Automatization software workflows with  CI/CD"         |
| [beautiful soup](https://www.crummy.com/software/BeautifulSoup/)            | "Library for pulling data out of HTML and XML files"    |
| [progress](https://pypi.org/project/progress/)                              | "Easy progress reporting for Python"                    |
