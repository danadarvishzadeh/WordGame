import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

from word_creator import *

"""
this script will check each word's correctness
from an online dictionary
"""


answers = []

append_lock = threading.Lock()

# lock the append function
def Appender(val, target):
    with append_lock:
        target.append(val)

# check the response of each request from the site to see 
# if the word is vaid
def Vajeh_Check(response, word):
    if response.status_code != '200':
        global status_flag
        status_flag = True
    soup = BeautifulSoup(response.text, 'html.parser')
    check_result = soup.find('div', attrs={'class':'fieldset'})
    if check_result:
        if check_result.text.strip() == 'جست‌وجوی دقیق':
            Appender(word, answers)
        else:
            pass
    else:
        pass


# making futures and running them by the rate of two
def Word_Check(word_list):
    status_flag = False
    with FuturesSession(max_workers=2) as session:
        futures = [session.get('http://www.vajehyab.com/?q=' + word + '&f=dehkhoda')
                for word in word_list]

        for future, word in zip(as_completed(futures), word_list):
            response = future.result()
            Vajeh_Check(response, word)