# Copyright (C) 2021 Korytov Pavel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import html
import os

import feedparser
from dotenv import load_dotenv
from feedgen.feed import FeedGenerator
from flask import Flask, request, abort
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


load_dotenv()
app = Flask(__name__)


@app.route('/<channel_id>')
def get(channel_id):
    if request.args['token'] != os.getenv('TOKEN'):
        abort(401)
        return
    d = feedparser.parse(
        f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    )
    fg = convert_feed(d)
    return fg.atom_str(pretty=True)
