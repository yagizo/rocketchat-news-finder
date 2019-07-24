#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import feedparser
import configparser
from dateutil.parser import parse
from pytz import timezone
import sqlite3
from rocketchat_API.rocketchat import RocketChat

def find_articles(
        rss_url,
        rc_url,
        rc_user,
        rc_password,
        rc_channel,
        rc_alias='yagizo',
        rc_icon=':new:',
        database='./feed.db',
        enable_post=True
        ):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS entries (published, link, tiltle)')

    rocket = RocketChat(rc_user, rc_password, server_url=rc_url)

    feeds = feedparser.parse(rss_url)
    for entry in feeds.entries:
        d = parse(entry.published).astimezone(timezone('Asia/Tokyo'))
        cur.execute('SELECT count(*) FROM entries WHERE link = ?', (entry.link, ))
        cnt = cur.fetchone()[0]
        if cnt == 0:
            print('[{}]{} ({})'.format(d.strftime("%Y/%m/%d"), entry.title, entry.link))
            cur.execute('INSERT INTO entries VALUES (?, ?, ?)', (d, entry.link, entry.title,))
            msg = '*{}* {}\n{}'.format(d.strftime("%Y/%m/%d"), entry.title, entry.link)
            if enable_post:
                rocket.chat_post_message(msg, channel=rc_channel, alias=rc_alias, emoji=rc_icon)

    con.commit()
    con.close()


def main(args):
    config = configparser.ConfigParser()
    config.add_section('basic_settings')
    config.add_section('rocket_chat')
    config.set('rocket_chat','alias','News Finder')
    config.set('rocket_chat','icon',':heavy_check_mark:')
    config.read(args.config)
    rss = config.get('basic_settings','rss_url')
    db = config.get('basic_settings','database')
    flag = True if config.get('basic_settings','enable_post') == True else False
    url = config.get('rocket_chat','url')
    user = config.get('rocket_chat','user')
    password = config.get('rocket_chat','password')
    channel = config.get('rocket_chat','channel')
    alias = config.get('rocket_chat', 'alias')
    icon = config.get('rocket_chat', 'icon')

    find_articles(rss, url, user, password, channel, rc_alias=alias, rc_icon=icon, database=db, enable_post=flag)
    exit(0)


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description="This is a tool for posting new articles on RocketChat.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument('-c', '--config', type=str, required=True, help='configuration file')

    exit(main(p.parse_args()))
