import requests
from flask import Flask, Response, request
from lxml import etree

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

    try:
        base_xml = requests.get(rss_url).content
        root = etree.fromstring(base_xml)

        #  Subordinate to the <rss> element is a single <channel> element.
        # @see https://validator.w3.org/feed/docs/rss2.html
        channel = root.xpath('/rss/channel')[0]
        items = channel.xpath('item')

        for item in items:
            titles = item.xpath('title')
            if titles and title_contains not in titles[0].text:
                channel.remove(item)

        return Response(etree.tostring(root), mimetype='text/xml')

    except Exception as e:
        return Response('Error: ' + e.__str__())


if __name__ == '__main__':
    app.run()
