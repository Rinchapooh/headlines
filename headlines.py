import datetime
import feedparser
import requests

from flask import Flask, render_template, request, make_response


app = Flask(__name__)

DEFAULTS = {
    'publication': 'bbc',
    'city': 'London',
    'currency_from': 'USD',
    'currency_to': 'KZT'
}

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640',
    'daily': 'http://www.dailymail.co.uk/home/index.rss'
}


@app.route("/")
def home():
    # Get customised headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    '''publication = request.args.get("publication")
     if not publication:
        publication = request.cookies.get("publication")
        if not publication:
           publication = DEFAULTS["publication"]
           '''
    articles = get_news(publication)

    # Get customised weather, based on user input or default
    city = get_value_with_fallback('city')
    weather = get_weather(city)

    # Get customized currency based on user input or default
    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, all_rates_keys = get_rate(currency_from, currency_to)

    # save cookies and return template
    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             feed_title=publication.upper() + ' ',
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             rates_keys=all_rates_keys))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']

    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']


def get_weather(city):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=8a691ca8687d5da894a462b99705f045"
    resp = requests.get(api_url)
    data = resp.json()
    weather = {'description': data["weather"][0]["description"],
               'temperature': data["main"]["temp"],
               'city': data["name"],
               'country': data['sys']['country'],
               'wind': data['wind']['speed']
               }
    return weather


def get_rate(frm, to):
    api_url = "https://openexchangerates.org/api/latest.json?app_id=70e97f32457f47d9b348254bc5da3978"
    resp = requests.get(api_url)
    data = resp.json()
    all_currency = (data['rates'])
    frm_rate = all_currency.get(frm.upper())
    to_rate = all_currency.get(to.upper())
    pretty_rate = round((to_rate / frm_rate), 2)
    keys_rates = sorted(all_currency.keys())
    return pretty_rate, keys_rates


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


if __name__ == '__main__':
    app.run(port=5000, debug=True)
