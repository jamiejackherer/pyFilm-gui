#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is the basic film-search configuration file.
"""
   
def title_dict():
    # Change this to choose dict file
    # a dict for common words to remove from the title
    title_dict = set(open('title_dict.txt').read().split()) 
