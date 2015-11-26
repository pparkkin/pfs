from lxml import html
import requests
from io import StringIO

class Scraper:
    SCORES_URL_PATTERN = '/years/%d/games.htm'
    def __init__(self, url_base, out_path):
        self._url_base = url_base
        self._out_path = out_path
    def scrape_games(self, y):
        fp = (self._out_path+'/%d-games.csv') % y
        url = (self._url_base + Scraper.SCORES_URL_PATTERN) % y
        print('scraping', url)
        page = requests.get(url)
        tree = html.fromstring(page.text)
        data = scrape_season(tree)
        print('writing', fp)
        with open(fp, 'w') as of:
            of.write(to_csv(y, data))


def is_home_win(tds):
    return tds[5].text == None

def is_tie(tds):
    return len(tds[4].xpath('strong')) == 0

def winning_team_score(tds):
    tie = is_tie(tds)
    if not tie:
        team_name = tds[4].xpath('strong/a')[0].text
        points = int(tds[7].xpath('strong')[0].text)
    else:
        team_name = tds[4].xpath('a')[0].text
        points = int(tds[7].text)

    return (team_name, points)

def losing_team_score(tds):
    team_name = tds[6].xpath('a')[0].text
    points = int(tds[8].text)
    return (team_name, points)

def scrape_scores(g):
    tds = g.xpath('child::td')

    (winning_team_name, winning_points) = winning_team_score(tds)
    (losing_team_name, losing_points) = losing_team_score(tds)

    home_win = is_home_win(tds)
    if home_win:
        return (losing_team_name, losing_points,
                winning_team_name, winning_points)
    else:
        return (winning_team_name, winning_points,
                losing_team_name, losing_points)

def _team_name(td):
    return td.xpath('a')[0].text

def _scrape_noscores(g):
    tds = g.xpath('child::td')

    visitor_team_name = _team_name(tds[3])
    home_team_name = _team_name(tds[5])

    return (visitor_team_name, None,
            home_team_name, None)

def scrape_week(g):
    return g.xpath('td')[0].text

def is_boxscore(g):
    bs = g.xpath('td[4]/a/text()')
    return len(bs) > 0 and bs[0] == 'boxscore'

def _scrape_games(gs):
    games = {}
    for g in gs:
        if not is_boxscore(g): continue ## FIXME: Record the game
        week = scrape_week(g)
        scores = scrape_scores(g)
        games[week] = games.get(week, []) + [scores]
    return games

def _scrape_games_left(gs):
    games = {}
    for g in gs:
        week = scrape_week(g)
        scores = _scrape_noscores(g)
        games[week] = games.get(week, []) + [scores]
    return games

def _merge_games(gs1, gs2):
    for k in gs2:
        gs1[k] = gs1.get(k, []) + gs2.get(k)
    return gs1

def scrape_season(tree):
    games_xpath = '//table[@id="games"]/tbody/tr[@class != "thead"]'
    games_trs = tree.xpath(games_xpath)
    games = _scrape_games(games_trs)
    gamesl_xpath = '//table[@id="games_left"]/tbody/tr[@class != " thead"]'
    gamesl_trs = tree.xpath(gamesl_xpath)
    gamesl = _scrape_games_left(gamesl_trs)
    return _merge_games(games, gamesl)

def _score_str(s):
    if s is None: return ''
    return str(s)

ROW_FORMAT = "%d,%s,%s,%s,%s,%s\n"
def to_csv(y, ss):
    out = StringIO()
    for w in sorted(ss.keys()):
        for g in ss[w]:
            visitor_name = g[0]
            visitor_score = _score_str(g[1])
            home_name = g[2]
            home_score = _score_str(g[3])
            row = ROW_FORMAT % (y, w,
                    visitor_name, visitor_score,
                    home_name, home_score)
            out.write(row)
    return out.getvalue()


