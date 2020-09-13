import feedparser
from feedgen.feed import FeedGenerator
from flask import Flask, Response

app = Flask(__name__)

# Phone name, format should be _$name_, found name in:
# https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/files/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12/
NAME = '_HMK30_'

# Base rss link, also satisfied with weekly release.
EU_MIUI_RSS = 'https://sourceforge.net/projects/xiaomi-eu-multilang-miui-roms/rss?' \
              'path=/xiaomi.eu/MIUI-STABLE-RELEASES/MIUIv12'


@app.route('/')
def eu_miui_filter():
    base_rss = feedparser.parse(EU_MIUI_RSS)
    for rss_entries in base_rss.entries:
        if NAME in rss_entries.title:
            # The Latest ROM's file name & download link.
            file_name = rss_entries.title.split('/')[-1]
            download_link = rss_entries.media_content[0]['url']

            # Create a feed.
            # https://github.com/lkiesow/python-feedgen#create-a-feed
            fg = FeedGenerator()
            fg.title('%s \'s eu MIUI' % (NAME,))
            fg.link(href='https://github.com/VergeDX')
            fg.description('Rss filter, writen by Vanilla. ')

            # Add feed entries.
            # https://github.com/lkiesow/python-feedgen#add-feed-entries
            fe = fg.add_entry()
            fe.title(file_name)
            fe.link(href=download_link)

            # Using response with mine type xml, avoid the browser parse.
            # https://stackoverflow.com/questions/11773348/python-flask-how-to-set-content-type
            return Response(fg.rss_str(pretty=True), mimetype='text/xml')


if __name__ == '__main__':
    app.run()
