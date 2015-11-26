import sys
import csv
from lxml import html
import requests
from io import StringIO

class Scraper:
    def __init__(self, url_base, out_path):
        self._url_base = url_base
        self._out_path = out_path
    def scrape_teams(self, y):
        fp = (self._out_path+'/%d-teams.csv') % y
        data_o = _scrape_teams_off(self._url_base, y)
        data_d = _scrape_teams_def(self._url_base, y)
        data = _merge_data(data_o, data_d)
        print('writing', fp)
        with open(fp, 'w') as of:
            of.write(to_csv(y, data))

OFF_VALS = [
    "team",
    "g",
    "points",
    "total_yards",
    "plays_offense",
    "yds_per_play_offense",
    "turnovers",
    "fumbles_lost",
    "first_down",
    "pass_cmp",
    "pass_att",
    "pass_yds",
    "pass_td",
    "pass_int",
    "pass_net_yds_per_att",
    "pass_fd",
    "rush_att",
    "rush_yds",
    "rush_td",
    "rush_yds_per_att",
    "rush_fd",
    "penalties",
    "penalties_yds",
    "pen_fd",
    ]

DEF_VALS = [
    "team",
    "points",
    "total_yards",
    "plays_offense",
    "yds_per_play_offense",
    "turnovers",
    "fumbles_lost",
    "first_down",
    "pass_cmp",
    "pass_att",
    "pass_yds",
    "pass_td",
    "pass_int",
    "pass_net_yds_per_att",
    "pass_fd",
    "rush_att",
    "rush_yds",
    "rush_td",
    "rush_yds_per_att",
    "rush_fd",
    "penalties",
    "penalties_yds",
    "pen_fd",
    ]

def scrape_indices(tree, table, vals):
    td_xpath = '//table[@id="'+table+'"]/thead/tr/th[@data-stat="%s"]/preceding-sibling::th'
    indices = []
    for v in vals:
        indices.append((len(tree.xpath(td_xpath % v)), v))
    return indices

def _scrape_value(i, k, td):
    if k == 'team':
        return td.xpath('a')[0].text
    else:
        return td.text

def scrape_values(tr, indices):
    tds = tr.xpath('td')
    v = [_scrape_value(i, k, tds[i]) for (i, k) in indices]
    return v

def scrape_stats(tree, vals):
    indices = scrape_indices(tree, 'team_stats', vals)
    trs = tree.xpath('//table[@id="team_stats"]/tbody/tr[@class != "average_table no_ranker"]')
    vals = [scrape_values(tr, indices) for tr in trs]

    stats = {}
    for t in vals:
        stats[t[0]] = t[1:]
    
    return stats

def _scrape_teams(y, url_pattern, vals):
    url = url_pattern % y
    print('scraping', url)
    page = requests.get(url)
    tree = html.fromstring(page.text)
    data = scrape_stats(tree, vals)
    return data

OFF_URL_PATTERN = '/years/%d/'
def _scrape_teams_off(url_base, y):
    return _scrape_teams(y, url_base+OFF_URL_PATTERN, OFF_VALS)

DEF_URL_PATTERN = '/years/%d/opp.htm'
def _scrape_teams_def(url_base, y):
    return _scrape_teams(y, url_base+DEF_URL_PATTERN, DEF_VALS)

def _merge_data(d1, d2):
    for k in d2:
        d1[k] = d1.get(k, []) + d2.get(k)
    return d1

OUT_FORMAT = ','.join(['%s' for i in range(len(OFF_VALS)+len(DEF_VALS)-1)])
def to_csv(y, stats):
    out = StringIO()
    for k in stats:
        vals = [k]+stats[k]
        line = OUT_FORMAT % tuple(vals)
        out.write(line)
        out.write('\n')
    return out.getvalue()

