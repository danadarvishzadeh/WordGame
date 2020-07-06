import re, sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

import word_creator

"""
this script will check each word's correctness
from an online dictionary
"""


answers = []
status_flag = False
append_lock = threading.Lock()


# lock the append function
def Appender(val, target):
    with append_lock:
        target.append(val)

# check the response of each request from the site to see 
# if the word is vaid
def Vajeh_Check(response, word, answers):
    if response.status_code != '200':
        global status_flag
        status_flag = True
    soup = BeautifulSoup(response.text, 'html.parser')
    check_result = soup.find('div', attrs={'class':'fieldset'})
    if check_result:
        if check_result.text.strip() == 'جست‌وجوی دقیق':
            Appender(word, answers)
            print('++++++')
      


# making futures and running them by the rate of two
def Word_Check(word_list, answers):
    with FuturesSession(max_workers=2) as session:
        futures = [session.request('GET', f'http://www.vajehyab.com/?q={word}&f=dehkhoda') for word in word_list]
        for future, word in zip(as_completed(futures), word_list):
            response = future.result()
            Vajeh_Check(response, word, answers)



def main():
    address = sys.argv[-1]
    with open(address, 'r') as f:
        f = f.read().strip().split(',')
        word_list = f[:-1].copy()
    Word_Check(word_list, answers)
    print('doneeeee!')
    print(status_flag)



if __name__ == '__main__':
    main()