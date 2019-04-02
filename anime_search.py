try:
    from difflib import get_close_matches
    from time import sleep
    import requests
    import os
    import re
except ModuleNotFoundError:
    print("Missing module, exiting.")
    sleep(2)
    exit(1)

def search(title):
    try:
        # test code to find closest match to title 
        lines = []
        with open("anime-000.txt", "r", encoding="utf8") as f:
            
            for line in f:
                try:
                    line = line.split(">")[2]
                    line = line.split("<")[0]
                    line = line.split("/")[5]
                    lines.append(line)
                except:
                    pass
            title = get_close_matches(title, lines, n=1)[0]
            
        with open("anime-000.txt", "r", encoding="utf8") as f:
            # regex to find id of anime
            try:
                pat = re.compile(r'<loc>https://myanimelist.net/anime/\d\d?\d?\d?\d?\d?/{}</loc>'.format(title))
            except UnicodeDecodeError:
                pass
            
            for line in f:
                try: 
                    match = re.findall(pat, line)
                except UnicodeDecodeError:
                    pass
                
                if match:
                    url = match[0]
                    animeID = re.search(r'anime/\d\d?\d?\d?\d?', url)
                    animeID = animeID.group().split("/")[1]
                    break

        info = requests.get("https://api.jikan.moe/anime/{}".format(str(animeID)))
        info = info.json()

        return info, url

    except Exception as e:
        print(str(e))
        sleep(3)
        return "missing", 0        