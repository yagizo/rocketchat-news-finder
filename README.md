# rocketchat-news-finder

## このツールは何？

お気に入りのサイト(のRSS)をチェックして新着記事をみつけたら、RocketChatの
任意のチャンネルにリンクを投稿してくれるツールです。

使い方は簡単。

収集元のサイトのRSSとRocketChatに関する設定を記述した設定ファイルを作成し
news-finder.py に指定して実行するだけです。


## 設定ファイル

まずは以下の設定ファイル(xxxxx.ini)を用意してください。

```
# news-finder settings

[basic_settings]
# 監視するサイトのRSSを設定する
rss_url=http://www.sample.com/news/feed

# 新着記事があった場合、Rocket.Chatに投稿するかどうか
#   True: 投稿モードが有効
#   False: 投稿モードが無効(データベースへのデータ登録のみ)
enable_post=True

# RSSの情報を保持するデータベース(SQLite)ファイルを指定する
database=./feed.db


[rocket_chat]
# Rocket.Chatの接続先URLを指定する
url=https://XXXXX.rocket.chat

# 使用するRocket.Chatのユーザー名
user=XXXXX

# 当該ユーザーのパスワード
password=XXXXX

# 投稿する先のチャンネル名
channel=XXXXX-channel

# 投稿者のエイリアスを設定
alias=News Finder

# 絵文字を設定
icon=:newspaper:
```

＃使い方

news-finder.py に 引数 `-c 設定ファイル` を指定して実行するだけ！

```
$ python ./news-finder.py -c xxxxx.ini
```

# 備考

news-finderはデータベース(SQLite)に既知の記事を登録し、実行するたびに差分をチェックして
新着記事があった時に、Rocket.Chatの任意のチャンネルに通知します。

cronなどで定期的に実行するなどの使い方に向いています。
