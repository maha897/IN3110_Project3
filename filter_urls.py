import re
from urllib.parse import urljoin

## -- Task 2 -- ##

def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Finds all the url links in a html text using regex.

    Args:
        html (str): 
            html string to parse
        base_url (str, optional):

        output (str, optional): 

    Returns:
        urls (set): 
            set with all the urls found in html text
    """

    # pattern for finding anchor tags in html code
    anchor_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
    # pattern for finding url in href attribute of anchor tags
    url_pat = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)
    urls = set()

    # find all urls in anchor tags
    for a in anchor_pat.findall(html):
        url = set(url_pat.findall(a))
        
        for url_ in url:
            if "#" in url_:
                url_ = url_.split("#")[0]

            if url_ != "":
                # add base-url if missing
                if url_.startswith("/"):
                    urls.add(urljoin(base_url, url_))
                else:
                    urls.add(url_)

    # write to file
    if output:
        print(f"Writing to: {output}")
        
        with open(output, 'w') as out:
            out.write(urls)

    return urls


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    
    Args:
        - text (str):
            the html text to parse
    Returns:
        - (set): 
            a set with urls to all the articles found
    """

    urls = find_urls(html)
    # pattern for generalised wikipedia wiki link
    pattern = r"(https*:\/\/)\w{2,3}\.(wikipedia\.org)\/wiki([\/\w+]+)"
    articles = set()
    
    for url in urls:
        if re.search(pattern, url):
            articles.add(url)

    # write to file
    if output:
        print(f"Writing to: {output}")
        
        with open(output, 'w') as out:
            out.write(articles)
    
    return articles


def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string.

    Args:
        html (str): 
            A string containing some HTML.

    Returns:
        src_set (set):
            A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """

    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()

    for img_tag in img_pat.findall(html):
        src = set(src_pat.findall(img_tag))

        for element in src:
            src_set.add(element)

    return src_set
