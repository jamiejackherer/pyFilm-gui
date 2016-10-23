#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   _  __      __           _
#  /  /__)    /_  . / _ _   /
# <  /    (/ /   / / / / /  >
# /_      /               _/

from bs4 import BeautifulSoup as BS # For parsing html and getting links
from hurry.filesize import size # To display filesize in MB instead of bytes
from google import scrape_with_config, GoogleSearchError
from time import gmtime, strftime # For our history file 
from gi.repository import Gtk
import requests as r
import pandas as pd # for parsing results.csv
import sys # For any system commands
import re # For regexing
import os

# create an instance of a requests session named 's'
s = r.Session()
# set the user agent and other stuff in the http header 
headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) Safari/9537.53", 
            "Accept":"text/q=0.9,image/webp,*/*;q=0.8", 
            "Accept-Language":"en-US,en"} 
# create an instance of the results file
csv_file = "results.csv"
# read said file
df = pd.read_csv(csv_file)
# get the vodlocker links from the file (you can also use df.['column-name']
vodlocker_link = df['link']
# get the title from the google link
link_id = df['title']
# get the number of results 
results = df['num_results_for_query']
# lower the letters of the results
results_lower = results[0].lower()

# users link choice from search_results_list
self.which_link = search_results.get_selection()
self.which_link.connect("changed", self.on_tree_selection_changed)


# find the film link
film = bs.find(type="video/mp4")
# get the actual film link
film_link = film["src"] 
# find the title as it is on the vodlocker page
title = bs.find(id="file_title").get_text() 
# prefix for file_name location
prfx = "downloaded_files/" 
# a dict of common words to remove from the title
title_dict = set(open('title_dict.txt').read().split()) 
# create a regex 'or' for items in the dict
regex_title = r"|".join(title_dict)
# make the title lowercase 
title_lower = fixed_title.lower()
# strip any white spaces from the lowered title
title_strip = title_lower.strip() 
# replace any spaces with hyphens 
title_hyphen = title_strip.replace(" ", "-")
# use the last 4 chars as the file extension 
ext = film_link[-4:] 

class Handler:
    def on_search_entry_activate():
        # prefix of search term
        site = "site:vodlocker.com " 
        # ask user for search term
        # TODO this needs to be from the entry box, use get_text() method
        keywords = site + entry.get_text()
        config = {
        'use_own_ip': True,                     # whether to use our own IP address 
        'keyword': keywords,
        'search_engines': ['google'],           # various configuration settings
        'num_pages_for_keyword': 1,
        'scrape_method': 'http',
        'do_caching': False,
        'num_results_per_page': 50,
        'log_level': 'CRITICAL',
        'output_filename': 'results.csv'        # file to save links to 
    #    'proxy_file': 'proxies.txt'            # file to load proixies from 
        }
        try:
            search = scrape_with_config(config)
        except GoogleSearchError as e:
            # TODO open error dialog aswell as printing error
            print(e)

    def on_quit_button_clicked(self, button):
        print("Quitting application")
        Gtk.main_quit()
   
    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print("You selected", model[treeiter][0])
                     
builder = Gtk.Builder() 
builder.add_from_file("ui.glade") 
builder.connect_signals(Handler()) 

window = builder.get_object("window1") 
entry = builder.get_object("search_entry") 
downloadbutton = builder.get_object("download_button")
searchbutton = builder.get_object("search_button")
found_links = builder.get_object("quit_button")
progress = builder.get_object("download_progress_bar")
progress = builder.get_object("status_bar")
found_links = builder.get_object("found_links_label")
search_results = builder.get_object("search_results_list")



window.connect("delete-event", Gtk.main_quit) 
window.show_all() 
Gtk.main()
