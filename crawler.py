from urlparse import urljoin

import argparse
import requests
from BeautifulSoup import BeautifulSoup


def crawl_page(url):
    """
    returns all URLs found on the page
    """
    urls = []
    try:
        html_page = requests.get(url).text
        soup = BeautifulSoup(html_page)
        # soup is an HTML tree object. see APIs in BeautifulSoup docs
        for link in soup.findAll('a'):
            href = link.get('href')
            # convert relative links to absolute URLs
            href = urljoin(url, href)
            if href.startswith('http'):  # avoid non http links like mailto,ftp
                href = href.split('#')[0]  # remove part after '#' from href
                urls.append(href)
    except Exception as e:
        # wildcard exception catching is usually not preferred but
        # here we cant afford to break the whole process just because of
        # some malformed HTML or wrong encoding, or for whatever reason

        # TODO: logging this to stderr would be a better idea
        print "crawling failed for %s | exception: %s" % (url, e)

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
    url_repo = run(args.seed, args.limit)

    for url in url_repo:
        print url.encode('utf-8')  # required for embedded Unicode chars in URL
    print "----------------------"
    print "Collected total %d URLs" % len(url_repo)
