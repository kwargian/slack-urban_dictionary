"""
Nathan Alderfer
6/20/2016
Slack slash command to fetch definition of a phrase from UrbanDictionary
"""

import logging
import requests
from bs4 import BeautifulSoup
import urlparse
import pprint

logger = logging.getLogger()
logger.setLevel(logging.INFO)

pp = pprint.PrettyPrinter()


def handler(event, context):
    request_data = urlparse.parse_qs(event['body'])
    logger.info('Received lookup request for term {}'.format(request_data['text'][0]))

    payload = {'term': request_data['text'][0]}
    r = requests.get('http://www.urbandictionary.com/define.php', params=payload)
    logger.debug(r.url)

    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content, 'html5lib')
        results = soup.find_all('div', 'meaning')
        logger.debug(results)

        logger.info('Returning response for term {}'.format(request_data['text'][0]))
        return {'response_type': 'in_channel',
                'text': results[0].text}
    else:
        logger.error('Lookup for term {} failed'.format(request_data['text'][0]))
        return {'response_type': 'ephemeral',
                'text': 'Loading UrbanDictionary definitions for this term was unsuccessful'}