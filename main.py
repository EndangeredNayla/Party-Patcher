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
    #if search == None:
    #    urlHack = "https://www.mariopartylegacy.com/forum-old/index.php?action=downloads;cat=3;sortby=mostview;orderby=desc;start=0"
    #else:
    urlHack = "https://www.mariopartylegacy.com/forum/search/1274/?q=" + search + "&t=resource&c[categories][0]=1&c[child_categories]=1&c[title_only]=1&o=date"
    response = requests.get(urlHack)
    soup = BeautifulSoup(response.content, 'html.parser')
    boardTitles = soup.find_all('h3', class_="contentRow-title")
    boardList = []
    for title in boardTitles:
        boardName = title.get_text()
        boardName = boardName.replace("MP1", "")
        boardName = boardName.replace("MP2", "")
        boardName = boardName.replace("MP3", "")
        boardName = boardName[1:]
        boardName = re.sub(r'\d\.\d', '', boardName)
        boardName = boardName[:-2]
        boardList.append(boardName)

    for boardName, url in zip(boardList, boardTitles):
        link_element = url.find('a')
        if link_element:
            boardID = re.findall(r'\d+', link_element['href'])[-1]
            downloadURL = "https://www.mariopartylegacy.com/forum/downloads/" + boardID + "/download"
            print("{}: {}".format(boardName, downloadURL))
if __name__ == "__main__":
    download_manifest(parse_args().search)