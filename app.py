import feedparser
from feedgen.feed import FeedGenerator
from flask import Flask, Response, request

app = Flask(__name__)


@app.route('/')
def rss_filter():
    rss_url = request.args.get('rss_url')
    title_contains = request.args.get('title_contains')

    # Need 2 args, or else show usage.
    if not (rss_url and title_contains):
        return 'Need rss_url & title_contains as query string, \n' \
               'this will return a new rss with title filter. \n' \
               '(Apply $title_contains for each item from $rss_url). '

    base_rss = feedparser.parse(rss_url)

    # No base_rss.feed, seems cannot fetch origin rss url.
    if not base_rss.feed:
        return 'Cannot fetch rss url\'s feed title, \n' \
               'please check the url: \n' + rss_url

    # Filtered rss entries.
    result_rss_entries = []
    for rss_entry in base_rss.entries:
        if title_contains in rss_entry.title:
            result_rss_entries.append(rss_entry)

    return build_rss_string(result_rss_entries, base_rss.feed.title, title_contains)


def build_rss_string(result_rss_entries, base_rss_title, title_contains):
    # Create a feed, https://github.com/lkiesow/python-feedgen#create-a-feed
    fg = FeedGenerator()
    fg.title('[%s] filtered [%s]' % (title_contains, base_rss_title))
    fg.link(href='https://github.com/VergeDX/rss_filter_server')
    fg.description('Rss filter, writen by HyDEV : )')

    for rss_entry in result_rss_entries:
        # Add feed entries.
        # https://github.com/lkiesow/python-feedgen#add-feed-entries
        fe = fg.add_entry()
        fe.title(rss_entry.title)
        fe.link(href=rss_entry.link)

    # Using response with mine type xml, avoid the browser parse.
    # https://stackoverflow.com/questions/11773348/python-flask-how-to-set-content-type
    return Response(fg.rss_str(pretty=True), mimetype='text/xml')


if __name__ == '__main__':
    app.run()
