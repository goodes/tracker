import logging
import simplejson
import requests
import os
logging.captureWarnings(True)

url = os.getenv('SLACK_URL')
def post(text, **kwargs):
    if url is None:
        print "No slack URL"
        return

    data = {
        'username': 'tracker',
        'text': text + "   @daniel",
        #'icon_url': 'https://pushover.net/icons/6FPsDRrkT5sM9Ar.png',
        "icon_emoji": ":package:",
        "mrkdwn": True,
    }
    data.update(kwargs)
    requests.post(url=url, data=simplejson.dumps(data))


# https://api.slack.com/docs/attachments
# {
#     "attachments": [
#         {
#             "fallback": "Required plain-text summary of the attachment.",
#
#             "color": "#36a64f",
#
#             "pretext": "Optional text that appears above the attachment block",
#
#             "author_name": "Bobby Tables",
#             "author_link": "http://flickr.com/bobby/",
#             "author_icon": "http://flickr.com/icons/bobby.jpg",
#
#             "title": "Slack API Documentation",
#             "title_link": "https://api.slack.com/",
#
#             "text": "Optional text that appears within the attachment",
#
#             "fields": [
#                 {
#                     "title": "Priority",
#                     "value": "High",
#                     "short": false
#                 }
#             ],
#
#             "image_url": "http://my-website.com/path/to/image.jpg",
#             "thumb_url": "http://example.com/path/to/thumb.png"
#         }
#     ]
# }
