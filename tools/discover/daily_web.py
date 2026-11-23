"""Read candidate hostnames and entry links from public HTML directories."""

import re
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup, ParserRejectedMarkup


GONGYI = 'https://gongyizhan.com'
PROVIDERS = 'https://www.apizhongzhuanzhan.com'
HOWTOK = 'https://howtok.net'
STATION_PATH = re.compile(r'/station/[a-z0-9][a-z0-9-]*/?')
SITE_PATH = re.compile(r'/site/[a-z0-9][a-z0-9-]*/')
# Some provider IDs contain dots, e.g. /providers/jeniya.cn.
PROVIDER_PATH = re.compile(r'/providers/[a-z0-9][a-z0-9_-]*(?:\.[a-z0-9][a-z0-9_-]*)*')
NON_SITE_DOMAINS = {
    'gongyizhan.com', 'apizhongzhuanzhan.com', 'howtok.net', 't.me', 'telegram.me', 'telegram.org',
    'discord.gg', 'discord.com', 'qq.com', 'weibo.com', 'x.com', 'twitter.com',
    'github.com', 'githubusercontent.com', 'jsdelivr.net', 'unpkg.com', 'cloudflare.com',
    'googleapis.com', 'gstatic.com', 'bit.ly', 't.co', 'tinyurl.com',
}
REDIRECT_PATH = re.compile(r'/(?:go|out|away|redirect|jump|url|track|click)(?:[/.]|$)', re.I)


def _rendered(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except ParserRejectedMarkup:
        return BeautifulSoup('', 'html.parser')
    for node in soup.select('template, noscript, [hidden], [aria-hidden="true"]'):
        node.decompose()
    return soup


def _one(node, selector):
    matches = node.select(selector, limit=2)
    return matches[0] if len(matches) == 1 else None


def _entry(link, origin, path_pattern):
    if link is not None:
        path = link['href'].removeprefix(origin)
        if path_pattern.fullmatch(path):
            return origin + path
    return None


def _external_host(host):
    # This value leaves the adapter as a bare host. The collector applies its
    # shared public-host policy after this source-specific filtering.
    try:
        host = host.lower().encode('idna').decode('ascii')
    except UnicodeError:
        return None
    if not re.fullmatch(r'(?:[a-z0-9-]+\.)+[a-z][a-z0-9-]*', host):
        return None
    if any(host == site or host.endswith('.' + site) for site in NON_SITE_DOMAINS):
        return None
    if host.split('.', 1)[0] in {'cdn', 'click', 'redirect', 'track', 'tracker'}:
        return None
    return host


def _website_host(href):
    if re.search(r'[\s\\\x00-\x1f\x7f]', href):
        return None
    try:
        url = urlsplit(href)
        host = url.hostname
    except ValueError:
        return None
    if url.scheme not in ('http', 'https') or not host or url.netloc.lower() != host:
        return None
    # Reject an outbound wrapper even when it occupies the website column.
    # Registration/referral URLs on the listed host contribute just the host.
    if REDIRECT_PATH.search(unquote(url.path)) or any(
        '//' in unquote(part) for part in (url.path, url.query, url.fragment)
    ):
        return None
    return _external_host(host)


def parse_gongyizhan(html):
    pairs = []
    for card in _rendered(html).select('#station-list > article.station-row'):
        domain = _one(card, '.st-id > .st-url')
        link = _one(card, '.st-id > .st-name-line > a.st-name[href]')
        page = _entry(link, GONGYI, SITE_PATH)
        if domain is None or not page:
            continue
        visible = domain.get_text(' ', strip=True).lower()
        if card.get('data-domain', visible).lower() != visible:
            continue
        host = _external_host(visible)
        if host:
            pairs.append((host, page))
    return pairs


def parse_apizhongzhuanzhan(html):
    pairs = []
    for table in _rendered(html).select('table'):
        headers = [th.get_text(strip=True) for th in table.select(':scope > thead > tr > th')]
        fields = ('平台', '官网', '类型')
        if any(headers.count(field) != 1 for field in fields):
            continue
        platform, website, kind = (headers.index(field) for field in fields)
        for row in table.select(':scope > tbody > tr'):
            cells = row.find_all('td', recursive=False)
            if len(cells) != len(headers) or cells[kind].get_text(strip=True) != '中转':
                continue
            page = _entry(_one(cells[platform], ':scope > a[href]'), PROVIDERS, PROVIDER_PATH)
            official = _one(cells[website], ':scope > a[href][aria-label^="访问 "][aria-label$=" 官网"]')
            if page and official is not None:
                host = _website_host(official['href'])
                if host:
                    pairs.append((host, page))
    return pairs


def parse_howtok(html):
    pairs = []
    # The sponsored grid is nested in a separate block before this heading.
    for grid in _rendered(html).select('#stations > section > div.grid'):
        previous = grid.find_previous_sibling()
        heading = previous.find('h2') if previous else None
        if not heading or heading.get_text(' ', strip=True).split()[:1] != ['全部中转站']:
            continue
        for card in grid.find_all('div', recursive=False):
            label = _one(card, 'p.truncate')
            detail = _entry(_one(card, 'a[href^="/station/"]'), HOWTOK, STATION_PATH)
            if label is not None and detail:
                host = _external_host(label.get_text(strip=True))
                if host:
                    pairs.append((host, detail))
    return pairs


WEB_SOURCES = {
    'howtok.net': (HOWTOK + '/', parse_howtok),
    'gongyizhan.com': (GONGYI + '/', parse_gongyizhan),
    'apizhongzhuanzhan.com': (PROVIDERS + '/providers', parse_apizhongzhuanzhan),
}
