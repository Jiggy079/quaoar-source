def top(limit):
    try:
        from time import sleep
        import requests
        import os
    except ModuleNotFoundError:
        print("Module missing, exiting.")
        sleep(2)
        exit(1)

    response = requests.get("https://api.jikan.moe/top/anime/1")
    top = response.json()
    top_list = []

    for i in range(0, int(limit)):
        title = (top["top"][i]["title"])
        rank = (str(top["top"][i]["rank"]))
        episodes = (str(top["top"][i]["episodes"]))
        score = (str(top["top"][i]["score"]))
        temp = title+"|"+rank+"|"+episodes+"|"+score
        top_list.append(temp)
    return top_list