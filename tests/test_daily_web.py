import unittest
from html import escape

from tools.discover.daily_web import WEB_SOURCES


GONGYI_URL, gongyi = WEB_SOURCES['gongyizhan.com']
PROVIDER_URL, providers = WEB_SOURCES['apizhongzhuanzhan.com']


def station(host='api.relay.test', entry='/site/relay/', visible=None):
    visible = host if visible is None else visible
    return f'''<article class="station-row" data-domain="{escape(host)}">
      <div class="st-id"><div class="st-name-line">
        <a class="st-name" href="{escape(entry)}">Brand</a></div>
        <div class="st-url mono">{escape(visible)}</div>
        <div class="st-badges"><a href="https://ads.test/">other.test</a></div>
      </div></article>'''


def stations(*cards):
    return '<section id="station-list" class="stations">' + ''.join(cards) + '</section>'


def official(url):
    return f'<a href="{escape(url)}" aria-label="访问 Relay 官网"><svg></svg></a>'


def row(website, entry='/providers/relay.cn', kind='中转'):
    return (f'<tr><td><a href="{escape(entry)}">Relay<span>优选</span></a></td>'
            f'<td>{website}</td><td>{kind}</td><td>noise.test</td></tr>')


def table(*rows, headings=('平台', '官网', '类型', '能力')):
    columns = ''.join(f'<th>{name}</th>' for name in headings)
    return f'<table><thead><tr>{columns}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


class DailyWebTests(unittest.TestCase):
    def test_feed_urls(self):
        self.assertEqual((GONGYI_URL, PROVIDER_URL),
                         ('https://gongyizhan.com/', 'https://www.apizhongzhuanzhan.com/providers'))

    def test_howtok_reads_only_visible_regular_cards_with_detail_links(self):
        url, parse = WEB_SOURCES['howtok.net']
        card = '<div><h3>Relay</h3><p class="truncate">real.test</p><a href="/station/real-test">详情</a></div>'
        other = card.replace('real.test', 'sponsor.test')
        body = ('<div id="stations"><section><div><h2>赞助推荐</h2><div class="grid">' + other +
                '</div></div><div><h2>全部中转站 <span>3 / 3</span></h2></div><div class="grid">' + card +
                card.replace('/station/', '/go/') + card.replace('class="truncate"', 'class="description"') +
                '</div></section></div>')
        self.assertEqual(parse(body), [('real.test', url + 'station/real-test')])
        self.assertEqual(parse(body.replace('全部中转站', '赞助推荐')), [])

    def test_visible_station_fields_only(self):
        html = station('ad.test') + stations(
            station('API.Relay.test'),
            station('xn--mkrw42a.com', GONGYI_URL + 'site/xn-mkrw42a/'),
            station('hidden.test', visible=''),
            station('conflict.test', visible='other.test'),
            station('broken.test', visible='a.test b.test'),
            station('bad.test').replace('class="st-name"', 'class="ad"'),
            station('notes.test').replace('class="st-url mono"', 'class="notes"'),
        )
        self.assertEqual(gongyi(html), [('api.relay.test', GONGYI_URL + 'site/relay/'),
                                      ('xn--mkrw42a.com', GONGYI_URL + 'site/xn-mkrw42a/')])

    def test_clean_provider_pairs_from_explicit_website_column(self):
        html = table(
            row(official('https://www.Relay.test/register?aff=discard#promo')),
            row(official('http://relay-two.test/models'), entry=PROVIDER_URL + '/relay-2'),
            row(official('https://vendor.test'), kind='官方'),
            row('-', entry='/providers/no-website'),
            row('<a href="https://tracker.test">广告</a>'),
            row(official('https://a.test') + official('https://b.test')),
        )
        self.assertEqual(providers(html), [('www.relay.test', PROVIDER_URL + '/relay.cn'),
                                          ('relay-two.test', PROVIDER_URL + '/relay-2')])

    def test_evidence_requires_exact_source_owned_entry(self):
        for parse, make_html, good in (
            (gongyi, lambda href: stations(station(entry=href)), '/site/relay/'),
            (providers, lambda href: table(row(official('https://relay.test'), entry=href)), '/providers/relay'),
        ):
            for href in ('', '/go?to=' + good, '//other.test' + good, 'https://other.test' + good,
                         'https://gongyizhan.com@other.test' + good, good + '?aff=abc', good + '#top',
                         good + '/more', good + '/../else', good + '%2fredirect', '/site/../'):
                with self.subTest(parser=parse.__name__, href=href):
                    self.assertEqual(parse(make_html(href)), [])

    def test_invalid_or_indirect_websites(self):
        bad = ('', 'javascript:open(1)', '//relay.test/', 'relay.test', '/go/relay',
               'https://apizhongzhuanzhan.com/go/relay', 'https://out.gongyizhan.com/relay',
               'https://wrapper.test/jump/abc', 'https://wrapper.test/?to=https%3A%2F%2Frelay.test',
               'https://t.me/s/relay', 'https://cdn.jsdelivr.net/logo.svg', 'https://bit.ly/abc',
               'https://user@relay.test/path', 'https://relay.test:bad', 'https://[oops',
               'https://relay.test\\@another.test', 'https://re\tlay.test', 'https://127.0.0.1')
        for href in bad:
            with self.subTest(href=href):
                self.assertEqual(providers(table(row(official(href)))), [])

    def test_ignore_drifted_or_hidden_lists_and_keep_row_associations(self):
        good = table(row(official('https://relay.test')))
        other = table(row(official('https://relay.test'), entry='/providers/another'))
        drifted = table(row(official('https://wrong.test')), headings=('平台', '广告', '类型', '能力'))
        ambiguous = table(row(official('https://wrong.test')), headings=('平台', '官网', '类型', '官网'))
        self.assertEqual(providers(good + '<template>' + other + '</template>' + drifted + ambiguous + other),
                         [('relay.test', PROVIDER_URL + '/relay.cn'), ('relay.test', PROVIDER_URL + '/another')])
        self.assertEqual(gongyi('<template>' + stations(station()) + '</template>'), [])

    def test_empty_malformed_and_offpage_text(self):
        for parse in (gongyi, providers):
            for html in ('', '<!DOCTYPE html><body>relay.test</body>', '<tr><td>relay.test',
                         '<script>"<a href=\"https://relay.test\">"</script>',
                         '<table><tbody><tr><td>中转</td></tr></tbody></table>'):
                with self.subTest(parser=parse.__name__, html=html):
                    self.assertEqual(parse(html), [])


if __name__ == '__main__':
    unittest.main()
