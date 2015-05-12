from index import app
from query import api_feed, reporter_list
from flask import render_template, request
from config import BASE_URL


@app.route('/')
def index():
    tags = [237184207]
    page_url = BASE_URL + request.path
    page_title = 'Campaign 2014'
    page_explainer = ["VPR's guide to the 2014 campaign season. Get our latest coverage, special features and election news apps all in one place."]
    stories = api_feed(tags, numResults=10, thumbnail=True)
    reporters = reporter_list(tags)

    featured = False
    #To add featured stories to right panel of topic page, add story API IDs
    #featured = api_feed([291752955, 292002570], numResults=2, thumbnail=True, sidebar=True)

    social = {
        'title': "",
        'subtitle': '',
        'img': '',
        'description': "",
        'twitter_text': "",
        'twitter_hashtag': ''
    }

    return render_template('content.html',
        page_title=page_title,
        page_explainer=page_explainer,
        stories=stories,
        social=social,
        featured=featured,
        reporters=reporters,
        page_url=page_url)
