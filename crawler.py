from urlparse import urljoin

import argparse
import requests
from BeautifulSoup import BeautifulSoup


def crawl_page(url):
    """
    returns all URLs found on the page
    """
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page)
    # soup is an HTML tree object. see APIs in BeautifulSoup docs
    urls = []
    for link in soup.findAll('a'):
        href = link.get('href')
        href = urljoin(url, href)  # to convert relative links to absolute URLs
        if href.startswith('http'):  # to avoid non http links like mailto, ftp
            href = href.split('#')[0]  # remove part after '#' from href
            urls.append(href)
    return urls


def run(seed, limit):
    """
    starts crawling from given seed URL, until `limit`
    number of pages are crawled or runs out of URLs.

    Args:
        seed: initial URLs to start crawling
        limit: maximum number of URLs that will be crawled

    Returns:
        A set of URLs
    """
    crawl_frontier = {seed}  # set of URLs to be crawled
    repository = set()  # set of URLs already crawled
    count = 0
    while crawl_frontier and count < limit:
        current_seed = crawl_frontier.pop()
        urls = crawl_page(current_seed)
        urls = set(urls) - repository  # exclude URLs already in repository
        crawl_frontier = crawl_frontier | urls  # union of both sets
        count += 1
        repository.add(current_seed)
    return (repository | crawl_frontier)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web Crawler script')
    parser.add_argument('-s', '--seed', required=True,
                        help="Initial seed URL, must be a valid full URL")
    parser.add_argument('-l', '--limit', type=int, default=10,
                        help="URLs to crawl before stopping")
    args = parser.parse_args()
    try:
        url_repo = run(args.seed, args.limit)
    except requests.exceptions.MissingSchema as e:
        print e
    # we can keep catching various exceptions here like above to
    # give nice n fancy message to end user instead of horrible traceback
    # exception handling should always be done in a code which is
    # "closest" to user interface

    for url in url_repo:
        print url.encode('utf-8')  # required for embedded Unicode chars in URL
    print "----------------------"
    print "Collected total %d URLs" % len(url_repo)
