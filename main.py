# ============================================
# PartyPlanner Parse
# Author: Nayla Hanegan (naylahanegan@gmail.com)
# Date: 6/29/23
# License: MIT
# ============================================

import argparse
import requests
import urllib.parse


def parse_args():
    parser = argparse.ArgumentParser(
        description='Technic Parser')
    parser.add_argument('-s', '--search', type=str, required=True, metavar="search", help='Parse Technic Search and give download URL.')
    args = parser.parse_args()
    return args

def download_manifest(search):
    url = "https://api.curse.tools/v1/cf/mods/search"
    params = {
    'gameId': '6351',
    'searchFilter': search
    }
    responce = requests.get(url, params=params)
    json = responce.json()
    for pack in json["data"]:
        url2 = "https://api.curse.tools/v1/cf/mods/" + str(pack["id"]) + "/files/" + str(pack["mainFileId"])
        responce = requests.get(url2)
        json2 = responce.json()
        print("{}: {}".format(pack["name"], "https://" + urllib.parse.quote(json2["data"]["downloadUrl"][8:])))
    if json["data"] == []:
        print("No Results")
if __name__ == "__main__":
    download_manifest(parse_args().search)