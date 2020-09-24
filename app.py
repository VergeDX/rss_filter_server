import requests
from feedgen.feed import FeedGenerator
from flask import Flask, Response, request
from lxml import etree

app = Flask(__name__)

# https://developer.github.com/v3/repos/releases/#get-the-latest-release
REPOS_API = 'https://api.github.com/repos/'
LATEST = '/releases/latest'


@app.route('/')
def api_usage():
    return Response('Usage: https://github.com/VergeDX/rss_filter_server/blob/master/README.md')


@app.route('/filter')
def rss_filter():
    # if not (rss_url and title_contains)
    if not ((rss_url := request.args.get('rss_url')) and (title_contains := request.args.get('title_contains'))):
        return api_usage()

    try:
        root = etree.fromstring(requests.get(rss_url).content)

        #  Subordinate to the <rss> element is a single <channel> element.
        # @see https://validator.w3.org/feed/docs/rss2.html
        channel = root.xpath('/rss/channel')[0]

        for item in channel.xpath('item'):
            titles = item.xpath('title')
            # noinspection PyUnboundLocalVariable
            if titles and title_contains not in titles[0].text:
                channel.remove(item)

        return Response(etree.tostring(root), mimetype='text/xml')

    except Exception as e:
        return Response('Error: ' + e.__str__())


@app.route('/github_releases')
def github_releases():
    if not (repos_arg := request.args.get('repos')):
        return api_usage()

    try:
        # https://github.com/lkiesow/python-feedgen#create-a-feed
        fg = FeedGenerator()

        # ValueError: Required fields not set (title, link, description)
        fg.title('GitHub multi-repo releases tracker')
        fg.link(href='https://github.com/VergeDX/rss_filter_server')
        fg.description('Tracker more repo\'s release in one rss link! '
                       'Written by HyDEV, thanks for using. ')

        # repos arg list to set, filtered same items.
        for repo_str in set(repos_arg.split(', ')):
            if 'message' not in (r_json := requests.get(REPOS_API + repo_str + LATEST).json()):
                # https://github.com/lkiesow/python-feedgen#add-feed-entries
                fe = fg.add_item()
                fe.title('[%s] %s' % (repo_str, r_json['name']))
                fe.link(href=r_json['html_url'])

        return Response(fg.rss_str(), mimetype='text/xml')

    except Exception as e:
        return Response('Error: ' + e.__str__())


if __name__ == '__main__':
    app.run()
