import pytest
from filter_urls import find_articles, find_img_src, find_urls
from requesting_urls import get_html

# Test some random urls


def test_find_urls():
    html = """
    <a href="#fragment-only">anchor link</a>
    <a id="some-id" href="/relative/path#fragment">relative link</a>
    <a href="//other.host/same-protocol">same-protocol link</a>
    <a href="https://example.com">absolute URL</a>
    """
    urls = find_urls(html, base_url="https://en.wikipedia.org")
    assert urls == {
        "https://en.wikipedia.org/relative/path",
        "https://other.host/same-protocol",
        "https://example.com",
    }


@pytest.mark.parametrize(
    "url, links",
    [
        ("https://en.wikipedia.org/wiki/Nobel_Prize", [
                'https://en.wikipedia.org/wiki/Oslo_Accords', 
                'https://en.wikipedia.org/wiki/Category:Official_website_different_in_Wikidata_and_Wikipedia', 
                'https://en.wikipedia.org/wiki/Ballistite'
            ]
        ),
        ("https://en.wikipedia.org/wiki/Bundesliga", [
                'https://en.wikipedia.org/wiki/FC_Erzgebirge_Aue', 
                'https://en.wikipedia.org/wiki/Berlin', 
                'https://en.wikipedia.org/wiki/Berliner_FC_Dynamo'
            ]
        ),
        (
            "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup", [
                'https://www.fis-ski.com/DB/general/results.html?sectorcode=AL&amp;raceid=100133', 
                'https://en.wikipedia.org/wiki/2020_Alpine_Skiing_World_Cup_%E2%80%93_Women%27s_Combined', 
                'https://en.wikipedia.org/wiki/International_Biathlon_Union'
            ]
        ),
    ],
)
def test_find_urls_pages(url, links):

    html = get_html(url)
    urls = find_urls(html)
    assert isinstance(urls, set)
    # print(urls)
    for url in urls:
        # make sure we've got full URLs
        assert not url.startswith("/")
        assert not url.startswith("#")
        assert " " not in url
        assert "://" in url
    for link in links:
        assert link in urls


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://en.wikipedia.org/wiki/Nobel_Prize", 
            [
                "https://en.wikipedia.org/wiki/Barack_Obama", 
                "https://en.wikipedia.org/wiki/Insulin", 
                "https://en.wikipedia.org/wiki/Radium"
            ]
        ),
        ("https://en.wikipedia.org/wiki/Bundesliga", 
            [
                "https://en.wikipedia.org/wiki/J.League", 
                "https://en.wikipedia.org/wiki/Eliteserien", 
                "https://ro.wikipedia.org/wiki/Bundesliga"
            ]
        ),
        ("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup", 
            [
                "https://en.wikipedia.org/wiki/Alpine_skiing", 
                "https://en.wikipedia.org/wiki/Winter_sport", 
                "https://en.wikipedia.org/wiki/Main_Page"
            ]
        )
    ],
)
def test_find_articles(url, expected):
    html = get_html(url)
    articles = find_articles(html)
    assert isinstance(articles, set)
    # TODO: more precise measure
    assert len(articles) > 10
    for article in articles:
        assert "://" in article
        proto, _, rest = article.partition("://")
        hostname, _, path = rest.partition("/")
        assert hostname.endswith("wikipedia.org"), f"Not a wikipedia link: {article}"
        assert path.startswith("wiki/"), f"Not a wikipedia article: {article}"

    # check expected articles are present
    for article in expected:
        assert article in articles


def test_find_img_src():
    html = """
    <img src="https://some.jpg">
    <img title="abc" src="/foo.png">
    <img nosrc>
    """
    src_set = find_img_src(html)
    assert src_set == {
        "https://some.jpg",
        "/foo.png",
    }
