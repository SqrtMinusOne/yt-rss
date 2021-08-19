import feedparser
import html
from feedgen.feed import FeedGenerator
from flask import Flask
from markupsafe import escape


def convert_feed(feed):
    fg = FeedGenerator()
    fg.id(feed['feed']['id'])
    fg.title(feed['feed']['title'])
    fg.author(name=feed['feed']['author'])
    fg.link(href=feed['feed']['link'], rel='alternate')

    for entry in feed['entries']:
        fe = fg.add_entry()

        fe.id(entry['id'])
        fe.author(name=entry['author'])
        fe.title(entry['title'])
        fe.link(href=entry['link'])
        summary = ''
        if entry['media_thumbnail']:
            summary += f'<img src="{entry["media_thumbnail"][0]["url"]}" />'

        data = html.escape(entry["summary"]).replace("\n", "<br />")
        summary += f'<p style="word-break:break-word;white-space:pre-wrap">{data}</p>'

        fe.content(content=summary, type='xhtml')
        fe.published(entry['published'])
        fe.updated(entry['updated'])

    return fg

app = Flask(__name__)


@app.route('/<channel_id>')
def get(channel_id):
    d = feedparser.parse(
        f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    )
    fg = convert_feed(d)
    return fg.atom_str(pretty=True)
