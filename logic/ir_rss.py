import feedparser

rss_url = "http://www.eltiempo.com/rss/"
feed = feedparser.parse(rss_url)
for post in feed:
    print(post.title)