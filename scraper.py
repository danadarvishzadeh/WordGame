import re, sys
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
status_flag = False
append_lock = threading.Lock()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'
}

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
            print('++++++')
        else:
            pass
    else:
        pass


# making futures and running them by the rate of two
def Word_Check(word_list):
    with FuturesSession(max_workers=2, ) as session:
        futures = [session.request('http://www.vajehyab.com/?q=' + word + '&f=dehkhoda', headers=headers)
                for word in word_list]

        for future, word in zip(as_completed(futures), word_list):
            response = future.result()
            Vajeh_Check(response, word)



def main():
    address = sys.argv[-1]
    with open(address, 'r') as f:
        f = f.read().strip().split(',')
        word_list = f[:-1].copy()
        word_count = int(f[-1])
    Word_Check(word_list)
    print('doneeeee!')
    address = address.split('.')[0]
    WordDump(address, answers)
    print(status_flag)



if __name__ == '__main__':
    main()