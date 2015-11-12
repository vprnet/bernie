#!/usr/bin/python
import json
import requests
from PIL import Image
from PIL import ImageOps
import urllib
import os
from bs4 import BeautifulSoup as Soup
from datetime import datetime
from cStringIO import StringIO
from config import NPR_API_KEY, ABSOLUTE_PATH
from collections import namedtuple


def api_feed(tag, numResults=1, char_limit=240, thumbnail=False, sidebar=False):
    """Query the NPR API using given tag ID, return dictionary of results"""

    Story = namedtuple("Story", "title date link image text byline audio landscape")

    stories = query_api(tag, numResults)

    story_list = []
    for story in stories:
        link = story['link'][0]['$text']
        date = convert_date(story['storyDate']['$text'])
        title = story['title']['$text'].strip()
        byline = get_byline(story)
        image, landscape = get_image_data(story)
        audio = get_audio_data(story)
        text = get_text(story, char_limit)
        if thumbnail:
            image = get_image_from_story(story)

        a_story = Story(title=title,
                        date=date,
                        link=link,
                        image=image,
                        text=text,
                        byline=byline,
                        audio=audio,
                        landscape=landscape)

        story_list.append(a_story)

    return story_list


def get_byline(story):
    try:
        byline = {}
        byline['name'] = story['byline'][0]['name']['$text']
        byline['url'] = story['byline'][0]['link'][0]['$text']
    except KeyError:
        byline = False

    return byline


def get_text(story, paragraphs_needed=1):
    """get first paragraph of story"""
    # if len(i) > 1 ignores paragraphs w/ no text, i.e. when images or audio
    full_text = [i['$text'] for i in story['text']['paragraph'] if len(i) > 1]
    text = full_text[:paragraphs_needed]

    return text


def get_audio_data(story):
    """if the story has audio, make a dict of its info"""
    try:
        audio = {}
        audio_file = story['audio'][0]
        audio['mp3'] = audio_file['format']['mp3'][0]['$text'].split('?')[0]
        audio['duration'] = audio_file['duration']['$text']
    except KeyError:
        audio = False

    return audio


def get_image_data(story):
    """if there's an image, determine orientation and define boundary"""
    try:
        story_image = story['image'][0]['crop'][0]
        image = story_image['src']
        width = int(story_image['width'])
        height = int(story_image['height'])
        if int(width) > int(height):
            landscape = True
            if width > 728:  # biggest size for landscape photos
                width = 728
        else:
            landscape = False
            if width > 223:  # biggest size for portrait photos
                width = 223
    except KeyError:
        image = False  # set equal to url string for default image
        landscape = False

    return image, landscape


def query_api(tag, numResults=10):
    """Hits the NPR API, returns JSON story list"""

    id_string = ','.join([str(s) for s in tag])
    query = ('http://api.npr.org/query?orgid=692' +
        '&fields=title,byline,storyDate,image,text,audio' +
        '&sort=dateDesc' +
        '&action=Or' +
        '&output=JSON' +
        '&numResults=%d' +
        '&id=%s' +
        '&apiKey=%s') % (numResults, id_string, NPR_API_KEY)

    r = requests.get(query)
    j = json.loads(r.text)
    stories = j['list']['story']

    return stories


def reporter_image(url):
    """Takes reporter URL from byline and returns URL to reporter's image"""

    r = requests.get(url)
    page = r.text
    soup = Soup(page)
    person_card = soup.find_all(id="person-card")[0]
    try:
        image = person_card.find_all('img')[0].get('src')
        thumbnail = generate_thumbnail(image, size=(100, 100))
    except IndexError:
        image = False
        thumbnail = False

    return thumbnail


def get_image_from_story(story):
    try:
        image_url = story['image'][0]['crop'][0]['src']
        if sidebar:
            image = generate_thumbnail(image_url, preserve_ratio=True, size=(326, 326))
        else:
            image = generate_thumbnail(image_url, preserve_ratio=True, size=(width, height))
    except KeyError:
        image = False

    return image


def generate_thumbnail(image_url, preserve_ratio=False, size=(220, 165)):
    """Take an image src, generate a thumbnail, return new path"""

    filename = image_url.rsplit('/', 1)[1]
    path_to_read = 'img/thumbnails/' + filename
    path_to_save = ABSOLUTE_PATH + 'static/' + path_to_read

    if not os.path.isfile(path_to_save):
        img_file = urllib.urlopen(image_url)
        img = StringIO(img_file.read())
        image = Image.open(img)
        if preserve_ratio:
            width = image.size[0]
            height = image.size[1]
            new_height = size[0] * height / width
            size = (size[0], new_height)
        im = ImageOps.fit(image, size, Image.ANTIALIAS)
        im.save(path_to_save)

    return path_to_read


def convert_date(timestamp):
    """Converts API timestamp to publication-ready dateline"""

    day = timestamp[5:7]
    month = datetime.strptime(timestamp[8:11], '%b').strftime('%B')
    year = timestamp[12:16]
    date = month + ' ' + day + ", " + year
    return date
