# ============================================
# PartyPlanner Parse
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 6/29/23
# License: MIT
# ============================================

import argparse
import requests
import re
import urllib.parse

from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser(
        description='Party Planner Parser')
    parser.add_argument('-s', '--search', type=str, required=True, metavar="search", help='Parse Party Planner Search and give download URL.')
    args = parser.parse_args()
    return args

def download_manifest(search):
    boardNameList = []
    boardURLList = []
    if search == None:
        urlHack = "https://www.mariopartylegacy.com/forum-old/index.php?action=downloads;cat=3;sortby=mostview;orderby=desc;start=0"
    else:
        urlHack = "https://www.mariopartylegacy.com/forum-old/index.php?action=downloads;cat=3;sortby=mostview;orderby=desc;start=0;sa=search2;searchfor=" + search
    response = requests.get(urlHack)
    soup = BeautifulSoup(response.content, 'html.parser')
    boardTitles = soup.find_all('tr', class_=["windowbg", "windowbg2"])
    for title in boardTitles:
        boardName = title.get_text()
        boardName = boardName.split("(None)")[0]
        boardName = boardName.strip()
        boardName = ' '.join([word for word in boardName.split() if not re.search(r'[123459789()]', word)])
        boardName = boardName.replace(" Mario Party Custom Boards", "")
    for url in boardTitles:
        link_element = url.find('a')
        if link_element:
            boardID = re.findall(r'\d+', link_element['href'])[-1]
            downloadURL = "https://www.mariopartylegacy.com/forum-old/index.php?action=downloads;sa=downfile&id=" + boardID
            print("{}: {}".format(boardName, downloadURL))
if __name__ == "__main__":
    download_manifest(parse_args().search)