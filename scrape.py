import sys
import os.path
import argparse

from scrape_season import Scraper

DESCRIPTION='Scrape NFL season data from the web'

def err_exit(msg, code):
    print(msg, file=sys.stderr)
    sys.exit(code)

def main(argv):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    # Workaround for required arguments printed as optional in
    # default help
    parser._optionals.title = "arguments"

    parser.add_argument('-b', '--base-url',
            dest='base_url',
            metavar='BASE_URL',
            help='Base URL of statistics website',
            required=True)
    parser.add_argument('-s', '--seasons',
            dest='seasons',
            metavar='SEASONS',
            help='Seasons to scrape',
            required=True)
    parser.add_argument('-o', '--output',
            dest='output',
            metavar='OUTPUT',
            help='Output directory',
            default='csv')

    args = parser.parse_args()

    scraper = Scraper(args.base_url, args.output)

    se = args.seasons.split(':')

    start = int(se[0])
    if len(se) < 2:
        end = int(se[0])
    else:
        end = int(se[1])

    for s in range(start, end+1):
        scraper.scrape_season(s)

if __name__ == '__main__':
    import sys
    main(sys.argv)

