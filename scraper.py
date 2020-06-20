import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

from cleaner import *

"""
this script will check each word's correctness
from an online dictionary
"""


answers = []

append_lock = threading.Lock()


def Appender(val, target):
    with append_lock:
        target.append(val)

def Vajeh_Check(response, word):
    soup = BeautifulSoup(response.text, 'html.parser')
    check_result = soup.find('div', attrs={'class':'fieldset'})
    if check_result:
        if check_result.text.strip() == 'جست‌وجوی دقیق':
            Appender(word, answers)
        else:
            pass
    else:
        pass

    
def Check(word_list):
    with FuturesSession(max_workers=2) as session:
        futures = [session.get('http://www.vajehyab.com/?q=' + word + '&f=dehkhoda')
                for word in word_list]

        for future, word in zip(as_completed(futures), word_list):
            response = future.result()
            Vajeh_Check(response, word)