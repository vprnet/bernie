from index import app
from query import api_feed
from flask import render_template, request
from config import BASE_URL


@app.route('/')
def index():
    tags = [182633668]
    page_url = BASE_URL + request.path
    page_title = "Totally Bernie"
    page_explainer = "Full Coverage Of Bernie Sanders' Presidential Run"
    underwriter_explainer = "Support From"
    audio_explainer = "Full Audio: Bernie Sanders Announces His Run For President"
    stories = api_feed(tags, numResults=10, thumbnail=True)
    featured1 = api_feed([403584370], numResults=1, thumbnail=True, sidebar=True)
    featured2 = api_feed([392561138], numResults=1, thumbnail=True, sidebar=True)

    social = {
        'title': "Totally Bernie",
        'subtitle': "Full Coverage Of Bernie Sanders' Presidential Run",
        'img': 'http://mediad.publicbroadcasting.net/p/vpr/files/styles/medium/public/201504/sanders-3-vpr-evancie-20141104.jpg',
        'description': "Campaign news, features and analysis from the news team at Vermont Public Radio.",
        'twitter_text': "Totally Bernie: Full Coverage Of Bernie Sanders' Presidential Run",
        'twitter_hashtag': "VT"
    }

    return render_template('content.html',
        page_title=page_title,
        page_explainer=page_explainer,
        underwriter_explainer=underwriter_explainer,
        audio_explainer=audio_explainer,
        stories=stories,
        social=social,
        featured1=featured1,
        featured2=featured2,
        page_url=page_url)
