import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

"""
this script will check each word's correctness
from an online dictionary
"""

inputs = input().strip().split(' ')

word_list = WordMaker(len(inputs), inputs)

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

    
start = datetime.datetime.now()

with FuturesSession(max_workers=2) as session:
    futures = [session.get('http://www.vajehyab.com/?q=' + word + '&f=dehkhoda')
              for word in word_list]
    prints = 0
    for future, word in zip(as_completed(futures), word_list):
        response = future.result()
        Vajeh_Check(response, word)
        prints += 1
    print(len(word_list), prints)
        
end = datetime.datetime.now()
print(end-start)
