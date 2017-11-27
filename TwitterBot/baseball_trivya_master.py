# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 18:40:10 2017

@author: Alexander
"""

from baseball_triviaBot import *
from credentials_BT import *

baseball_trivya = BaseballTrivia(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, FB_URL)

while True:
    baseball_trivya.doAction()