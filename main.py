import platform
import requests
import re
import shutil
import subprocess
import os
from tkinter import filedialog
import urllib.parse

from bs4 import BeautifulSoup

def get_filename_from_cd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def download_manifest(search):
    boardNameList = []
    boardURLList = []
    urlHack = "https://www.mariopartylegacy.com/forum/search/search?search_type=resource&keywords=" + search + "&t=resource&c[categories][0]=1&c[nodes]=1&c[title_only]=1&o=date"
    response = requests.get(urlHack)
    soup = BeautifulSoup(response.content, 'html.parser')
    boardTitles = soup.find_all('h3', class_="contentRow-title")
    boardList = []
    for title in boardTitles:
        boardName = title.get_text()
        boardName = boardName.replace("MP1", "Mario Party 1 - ")
        boardName = boardName.replace("MP2", "Mario Party 2 - ")
        boardName = boardName.replace("MP3", "Mario Party 3 - ")
        boardName = boardName[1:]
        boardName = re.sub(r'\d\.\d', '', boardName)
        boardName = boardName[:-2]
        boardList.append(boardName)

    options = []
    for boardName, url in zip(boardList, boardTitles):
        link_element = url.find('a')
        if link_element:
            boardID = re.findall(r'\d+', link_element['href'])[-1]
            downloadURL = "https://www.mariopartylegacy.com/forum/downloads/" + boardID + "/download"
            options.append((boardName, downloadURL))

    if options:
        print("Select a board:")
        for i, (boardName, downloadURL) in enumerate(options):
            print(f"{i + 1}: {boardName}")
        
        while True:
            try:
                choice = int(input("Enter the number of your choice: "))
                if 1 <= choice <= len(options):
                    selected_option = options[choice - 1]
                    print(f"You selected: {selected_option[0]}")
                    r = requests.get(selected_option[1], allow_redirects=True)
                    try:
                        os.mkdir('.tmp/')
                    except:
                        pass
                    filename = get_filename_from_cd(r.headers.get('content-disposition'))
                    open(".tmp/" + filename[1:-1], 'wb').write(r.content)
                    print(f"Download Completed: {selected_option[0]}")
                    file_path = filedialog.askopenfilename(title="Select the Base ROM", filetypes=[("Base ROM", "*.z64")])
                    pp64Link = "https://github.com/PartyPlanner64/PartyPlanner64/releases/download/v0.8.2/partyplanner64-cli-win.exe"
                    try:
                        os.mkdir('bin/')
                    except:
                        pass
                    r2 = requests.get(pp64Link, allow_redirects=True)
                    open("bin/partyplanner-cli.exe", 'wb').write(r2.content)
                    if platform.system() != "Windows":
                        subprocess.run(["wine", "bin/partyplanner-cli.exe", "overwrite", "--rom-file", file_path, "--target-board-index", "0", "--board-file", ".tmp/" + filename[1:-1], "--output-file", ".tmp/patch.z64"])
                    elif platform.system() == "Windows":
                        subprocess.run(["bin/partyplanner-cli.exe", "overwrite", "--rom-file", file_path, "--target-board-index", "0", "--board-file", ".tmp/" + filename[1:-1], "--output-file", ".tmp/patch.z64"])
                    elif
                        break
                    file_path2 = filedialog.asksaveasfilename(title="Select the Output ROM", filetypes=[("Patched ROM", "*.z64")])
                    os.rename('.tmp/patch.z64', file_path2)
                    shutil.rmtree(".tmp")
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    else:
        print("No matching download URLs found.")

if __name__ == "__main__":
    search_query = input("What board are you search for: ")
    download_manifest(search_query)