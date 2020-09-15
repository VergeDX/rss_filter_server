import lxml
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
    except requests.exceptions.MissingSchema as e:
        return Response(e.__str__())

    try:
        root = etree.fromstring(base_xml)
    except lxml.etree.XMLSyntaxError as e:
        return Response('Link may not xml: ' + e.__str__())

    if root[0].tag != 'channel':
        return Response('Link %s may not rss. ' % (rss_url,))

    for child in root[0]:
        # TODO: child[0] should be title...?
        if child.tag == 'item' and title_contains not in child[0].text:
            root[0].remove(child)

    return Response(etree.tostring(root), mimetype='text/xml')


if __name__ == '__main__':
    app.run()
