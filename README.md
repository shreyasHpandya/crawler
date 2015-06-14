# A Web Crawler

This is a simple script that does the very basic crawling. It takes one seed URL and starts crawling until either it hits the supplied limit or it runs out of URLs to crawl. It prints out the list of all URLs gathered.

##Tty it out

`git clone https://github.com/shreyasHpandya/crawler.git`

`pip install requirements.txt`

optionally do this in fresh [virtualenv](https://virtualenv.pypa.io)


    $ python crawler.py -h
    usage: crawler.py [-h] -s SEED [-l LIMIT]

    Web Crawler script

    optional arguments:
        -h, --help
              Show this help message and exit
        -s SEED, --seed SEED
              Initial seed URL, must be a valid full URL
        -l LIMIT, --limit LIMIT
              URLs to crawl before stoping


Example:

    $ python crawler.py -s http://python.org -l 20
