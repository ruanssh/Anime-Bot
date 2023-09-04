import discord
from discord.ext import commands
import requests
import asyncio
import os

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="!")

@bot.command(name="anime")
async def anime(ctx, *, nome_anime: str): 
    message = (
        "Escolha o tipo:\n"
        "1. **Anime**\n"
        "2. **Movie**\n"
        "3. **Ova**"
    )
    await ctx.send(message)

    def check(response):
        return response.author == ctx.author and response.channel == ctx.channel and response.content in ["1", "2"]

    try:
        response = await bot.wait_for("message", check=check, timeout=30.0)

        if response.content == "1":
            query_type = "tv"
        elif response.content == "2":
            query_type = "movie"
        elif response.content == "3":
            query_type = "movie"
        else:
            await ctx.send("Escolha inválida. Use `!anime` novamente para selecionar um tipo válido.")
            return

        url = f"https://api.jikan.moe/v4/anime?q={nome_anime}&type={query_type}"

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP error
        data = response.json()

        title = data["data"][0]["title"]
        studio = data['data'][0]['studios'][0]['name']
        status = data['data'][0]['status']
        score = data['data'][0]['score'] 
        popularity = data['data'][0]['popularity'] 
        synopsis = data['data'][0]['synopsis'] 
        max_length_synopsis = 200

        if len(synopsis) > max_length_synopsis: # limits synopsis range
            truncated_text = synopsis[:max_length_synopsis] + "[...]"
        else:
            truncated_text = synopsis

        embed = discord.Embed(
            title=f"{title}",
            color=discord.Color.red() 
        )

        embed.set_image(url=data['data'][0]['images']["jpg"]["large_image_url"])
        
        embed.add_field(name="Status:", value=status, inline=True)
        embed.add_field(name="Studio:", value=studio, inline=True)

        embed.add_field(name="\u200B", value="\u200B", inline=True)

        embed.add_field(name="Popularity:", value=popularity, inline=True)
        embed.add_field(name="Score:", value=score, inline=True)

        embed.add_field(name="\u200B", value="\u200B", inline=True)
       
        embed.set_footer(text=truncated_text, icon_url="https://i.imgur.com/maGXbSJ.png")

        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("Tempo limite para escolha expirado. Use `!anime` novamente para selecionar um tipo.")
    
    except requests.RequestException as e:
        await ctx.send(f"Ocorreu um erro ao acessar a API: {str(e)}")
    
    except (KeyError, IndexError):
        await ctx.send("Não foi possível encontrar informações sobre o anime.")

bot.run(os.getenv("BOT_TOKEN"))
