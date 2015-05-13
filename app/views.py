from index import app
from query import api_feed, reporter_list
from flask import render_template, request
from config import BASE_URL


@app.route('/')
def index():
    tags = [182633668]
    page_url = BASE_URL + request.path
    page_title = 'Bernie'
    page_explainer = ["VPR's guide to all things Bernie Sanders."]
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
