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
import sys # For any system commands
import re # For regexing
import os

class Handler:
    def search_google():
        # prefix of search term
        site = "site:vodlocker.com " 
        # ask user for search term
        # TODO this needs to be from the entry box, use get_text() method
        keywords = site + input("{0}\n|{1}[?] {2}Enter a film title to search for.." \
                                "\n|\n|{3}--> {4}".format(lb, O, W, B, W)) 
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

        s = r.Session() # create an instance of a requests session named 's'
        headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) Safari/9537.53", 
                    "Accept":"text/q=0.9,image/webp,*/*;q=0.8", 
                    "Accept-Language":"en-US,en"} # set the user agent and other stuff in the http header 
        
        csv_file = "results.csv" # create an instance of the file
        df = pd.read_csv(csv_file) # read said file
        vodlocker_link = df['link'] # get the vodlocker links from the file (note: you can also use df.['column-name']
        link_id = df['title']
        results = df['num_results_for_query']
        results_lower = results[0].lower()
        
        # print how many links found in how many secs
        # TODO these should be displayed in a scrolled window                
        print("{0}\n|{1}[+] {2}We have found {3}\n{2}".format(lb, G, W, results_lower)) 
        print(link_id) # print the title of the pages found as shown in google    
        """We need to use the link that the user chooses' from the list.

        If the vodlocker page does not contain a link to a video
        we come back and ask the user to choose again.
        """     
        # Variables for get_film_link function.
        # TODO 
        which_link = input("{0}\n|{1}[?] {3}Which vodlocker link should we " \
                       "use?\n|\n|{2}--> {3}".format(lb, O, B, W))   
        while True:
            # Get the film link using 'which_link' given by the user and
            # iterate over until we find a valid page with a link in
            req = s.get(vodlocker_link[int(which_link)], headers=headers) 
            bs = BS(req.text, "lxml") # create a soup object
           #file_removed = r"^http?://(*.*.*.*)/([a-zA-Z0-9]\+\)(v.mp4)" 
            # TODO it will be better if we can use a
            # regex search to search for a link 
            # (e.g., http://177.272.45.91/vhxjhvjhv89dyf9s8eyuf98syfhs89y/v.mp4) 
            # instead of .mp4 
            
            # If this is not in the page then we dont want this page
            file_removed = "v.mp4" 
            if file_removed not in bs:
                # Print no video file
                print("{0}\n|{1}[!] {2}We could not find a video file." \
                      .format(lb, R, W)) 
            else:
                break
        
        film = bs.find(type="video/mp4") # find the film link
        film_link = film["src"] # get the actual film link
        title = bs.find(id="file_title").get_text() # find the title as it is on the vodlocker page
        title_dict() # title_dict from conf file
        regex_title = r"|".join(title_dict) # create a regex 'or' for items in the dict
        fixed_title = re.sub(regex_title, "",title, flags=re.I) # actually remove the items that are in 'title_dict'
        print("{0}\n|{1}[+]{2} The title of the film is:\n|\t{3}".format(lb, G, W, fixed_title)) # print the title with words from 'title_dict' removed
        print("{0}\n|{1}[+]{2} We found a video link on the vodlocker page:\n|\t{3}".format(lb, G, W, film_link)) # 

        title_lower = fixed_title.lower() # make the title lowercase
        title_strip = title_lower.strip() # strip any white spaces from the lowered title
        title_hyphen = title_strip.replace(" ", "-") # replace any spaces with hyphens    
        ext = film_link[-4:] # use the last 4 chars as the file extension (this should be .mp4 or other video ext.) 
        while True:
            file_name = title_hyphen + ext # name the file by putting 
            file_name_ok = input("{0}\n|{1}[+] {2}We have attempted to name the file from the title; \n|\t\"{3}\"\n|Is our guess O.K? [Yes/no]\n|{4}--> {5}".format(lb, G, W, file_name, B, W)) # ask user if our file_name guess is ok, if no then the user can choose a file_name
            if file_name_ok == 'yes':
                continue
            if file_name_ok != 'yes':
                file_name = input("{0}\n|{1}[+] {2}Please name the file:\n|\n|{3}--> {4}".format(lb, G, W, B, W)) + ext
                continue
            else:
                continue    
                
        prfx = "downloaded_files/" # prefix for file_name location
        title_dict = set(open('title_dict.txt').read().split()) # a dict for common words to remove from the title
        
        u = s.get(film_link, headers=headers, stream=True) # create an instance of the file stream
        file_size = int(u.headers["content-length"]) # get meta info -- file size
        print("{0}\n|{1}[+] {2}File Path and name:\n|\n|\t\"{3}{4}\"".format(lb, G, W, prfx, file_name)) # print the file name and path
        print("{0}\n|{1}[+] {2}File Size: {3}".format(lb, G, W, size(file_size))) # print the file size
        bar = ProgBar(file_size / 1024, title=lb + "\n|" + G + " [+] " + W + "Downloading:\n|\n|" + file_name + "\n" + lb, stream=sys.stdout, bar_char='█', update_interval=1) # Progress bar 
        with open(prfx + file_name, 'wb') as f:
            dl = 0
            if file_size is None: # no content length header
                f.write(r.content)
                print(lb)
                raise Exception("\n|{0}[!] {1}We could not get the total file size (this means there is no data to write to a file).".format(R, W)) # error for no data
            else:
                for chunk in u.iter_content(1024):
                    dl += len(chunk)
                    f.write(chunk)
                    f.flush()
                    bar.update(item_id = file_name)
            print("{0}\n|{1}[+] {2}Finished downloading {3}\n".format(lb, G, W, file_name))
            
            
window.connect("delete-event", Gtk.main_quit) 
window.show_all() 
Gtk.main()
