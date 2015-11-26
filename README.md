Scrape NFL Game and Team Data from the Web
------------------------------------------

Python script to scrape NFL game and team data from the web and store it into CSV files.

## Usage

    usage: scrape.py [-h] -b BASE_URL -s SEASONS [-o OUTPUT]

    Scrape NFL season data from the web

    arguments:
    -h, --help            show this help message and exit
    -b BASE_URL, --base-url BASE_URL
                            Base URL of statistics website
    -s SEASONS, --seasons SEASONS
                            Seasons to scrape
    -o OUTPUT, --output OUTPUT
                            Output directory

## Example Usage

    python scrape.py -b http://www.pro-football-reference.com -s 1992:1993 -o csvtest
