from index import app
from query import api_feed
from flask import render_template, request
from config import BASE_URL


@app.route('/')
def index():
    tags = [182633668]
    page_url = BASE_URL + request.path
    page_title = "Following Bernie: A VPR Exclusive"
    page_explainer = ["VPR's guide to all things Bernie Sanders."]
    underwriter_explainer = "Brought to you by:"
    audio_explainer = "Bernie Announces His Run for President"
    stories = api_feed(tags, numResults=10, thumbnail=True)
    featured = api_feed([392561138, 403584370], numResults=2, thumbnail=True, sidebar=True)

    social = {
        'title': "Following Bernie",
        'subtitle': "A VPR Exclusive",
        'img': '',
        'description': "Follow Bernie with VPR",
        'twitter_text': "Follow Bernie with VPR",
        'twitter_hashtag': ""
    }

    return render_template('content.html',
        page_title=page_title,
        page_explainer=page_explainer,
        underwriter_explainer=underwriter_explainer,
        audio_explainer=audio_explainer,
        stories=stories,
        social=social,
        featured=featured,
        page_url=page_url)
