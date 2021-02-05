"""
user_image_dump.py
Quick and dirty script to retrieve images submitted by a user and dump them to single HTML file
"""

import requests
import requests.auth
import settings
import logging
import json
import time

# get access token from reddit service
client_auth = requests.auth.HTTPBasicAuth(settings.APP_ID, settings.APP_SECRET)
post_data = { 'grant_type' : 'password', 'username': settings.USER_ID, 'password': settings.USER_PASS }
headers = { 'User-Agent': 'WtfClient/0.1 by wtf' }
response  = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=post_data, headers=headers)

if 'access_token' not in response.json():
        logging.fatal("Unexpected response: {0}".format(response.json()))

token_type = response.json()['token_type']
access_token = response.json()['access_token']

# use access token to retrieve user submissions
urls = []
after = None
while True:

    headers = {'Authorization': '{0} {1}'.format(token_type, access_token), 'User-Agent': 'WtfClient/0.1 by wtf'}
    params = {'count': 100, 'show': 'given', 'sort': 'new'}
    if after is not None:
        params['after'] = after

    response = requests.get('https://oauth.reddit.com/user/{0}/submitted'.format(settings.TEST_ACCOUNT), headers=headers, params=params)
    response_dict = response.json()

    for child in response_dict['data']['children']:
        url = child['data']['url']
        if url not in urls:
            urls.append(url)

    after = response_dict['data']['after']
    if after is None:
        break

    time.sleep(1)

# dump user submitted images to html file
with open("{0}.html".format(settings.TEST_ACCOUNT), 'w') as fh:
    fh.write('<div style="text-align: center; background-color: #696969"\n>')
    for url in urls:
        try:
            ext = url.split('.')[-1]
            if ext.lower() in ['png', 'jpg', 'jpeg', 'gif', 'svg', 'pjp', 'pjpeg', 'avif', 'apng', 'webp']:
                fh.write('<a href="{0}"><img src="{0}", width=60%></a><br><br>\n'.format(url))
        except:
            continue
    fh.write('</div>')

print("HTML file writen...") 
