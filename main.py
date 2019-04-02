try:
    from time import sleep
    import discord
    from discord.ext import commands
    from discord.ext.commands import Bot
    import asyncio
    import os
    import anime_search
    import anime_top
except ModuleNotFoundError:
    print("Missing module, exiting.")
    sleep(2)
    exit(1)

bot = commands.Bot(command_prefix="&")

@bot.event
async def on_ready():
    print("MAL Bot ready")
    print("Username: {}".format(bot.user.name))
    print("ID: {}\n".format(bot.user.id))
    await bot.change_presence(game=discord.Game(name="Type &printhelp | {} servers".format(str(len(list(bot.servers))))))
    with open("servers.txt", "w+", encoding="utf8") as f:
        f.write("SERVER LIST\n\n")
        for server in list(bot.servers):
            f.write(str(server)+"\n")

@bot.event
async def on_server_join(server):
    await bot.change_presence(game=discord.Game(name="Type &printhelp | {} servers".format(str(len(list(bot.servers))))))
    with open("servers.txt", "w+", encoding="utf8") as f:
        f.write("SERVER LIST\n\n")
        for server in list(bot.servers):
            f.write(str(server)+"\n")

@bot.event
async def on_server_remove(server):
    await bot.change_presence(game=discord.Game(name="Type &printhelp | {} servers".format(str(len(list(bot.servers))))))
    with open("servers.txt", "w+", encoding="utf8") as f:
        f.write("SERVER LIST\n\n")
        for server in list(bot.servers):
            f.write(str(server)+"\n")

@bot.command(pass_context=True)
async def search(ctx, *args):
    try:
        missing = False
        title = ""
        count = 0
        for i in range(len(args)-1):
            title += args[count].capitalize()+" "
            count += 1
        title += args[-1].capitalize()
        print("Searched for: {}".format(title))
        title = title.replace(" ", "_")

        missing = False
        info, url = anime_search.search(title)

        if info == "missing": missing = True

        if missing == False:
            episodes = str(info["episodes"])
            title = info["title"]
            animeType = info["type"]
            thumbnail = info["image_url"]
            premiered = str(info["premiered"])
            status = info["status"]
            score = str(info["score"])
            popularity = str(info["popularity"])
            synopsis = info["synopsis"]
            url = url.strip("<loc>")
            url = url.strip("</loc>")
            link = url



            embed = discord.Embed(title="Anime Information", colour=0x21ff00)
            embed.set_thumbnail(url=thumbnail)
            embed.add_field(name="Title", value=title, inline=False)
            embed.add_field(name="Episodes", value=episodes, inline=False)
            embed.add_field(name="Type", value=animeType, inline=False)
            embed.add_field(name="Status", value=status, inline=False)
            embed.add_field(name="Premiered", value=premiered, inline=False)
            embed.add_field(name="Score", value=score, inline=False)
            embed.add_field(name="Popularity", value="#"+popularity, inline=False)
            embed.add_field(name="Link", value=link, inline=False)
            
            await bot.say(embed=embed)

            await bot.say("**Synopsis**\n")

            if len(synopsis) > 2000:
                await bot.say("*Too long, please open anime in MAL if you wish to read it.*")
            
            else:
                await bot.say(synopsis)

            # old code for sending synopsis, no longer used
            # synopsisList = []
            # for line in synopsis.split(". "):
            #     synopsisList.append(line)
            
            # mid = len(synopsisList) // 2
            # text = ""
            # for i in range(0, mid):
            #     text += synopsisList[i] +". "
            # await bot.say(text)
            # text = ""
            # for i in range(mid+1, len(synopsisList)):
            #     text += synopsisList[i] + ". "
            # await bot.say(text)
        else:
            await bot.say("Anime not found D:")
    except Exception:
        pass

@bot.command(pass_context=True)
async def top(ctx, limit):
    if int(limit) > 25:
        limit = str(25)

    top_list = anime_top.top(limit)
    
    embed = discord.Embed(title="Top {} Anime".format(limit), colour=0x21ff00)
    for anime in top_list:
        info = anime.split("|")
        embed.add_field(name="#{} {}".format(info[1], info[0]), value="Score: {}  \nEpisodes: {}".format(info[3], info[2]), inline=False)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def printhelp(ctx):
    embed = discord.Embed(title="Quaoar Commands", colour=0x21ff00)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="&search (anime)", value="Search MyAnimeList for the specified anime and output some stuff about it")
    embed.add_field(name="&top (limit)", value="Show the top rated anime up to and including specified limit (max 25)")
    embed.add_field(name="&printhelp", value="Displays this help menu")
    embed.set_footer(text="Quaoar v0.0.2 | By Jiggy  ^ ^")
    await bot.say(embed=embed)

#bot.run(token goes here)
