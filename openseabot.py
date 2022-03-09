import discord
from discord import embeds
from discord.ext import commands
from osAPI import *
from config import *
import datetime

class OpenSeaBot(commands.Cog):
    def __init__(self , bot):
        self.bot = bot 
        self.cName = collection_name

    @commands.Cog.listener()
    async def on_ready(self):
        print("Open Sea bot is now online")
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")
    @commands.command()
    async def floor(self , ctx):
        try:
            floor = get_floor(self.cName)
            await ctx.send(f'Floor Price of {self.cName}: {floor} {emoji_id}')
        except:
            await ctx.send("Please try Again")
    @commands.command()
    async def trait(self, ctx, token):
        try:
            traits = get_traits(self.cName , token)
            img = get_image(self.cName,token)
            counts = get_counts(self.cName,token)
            embeds = parse_traits(traits , token,img,counts)
            embeds.color = embed_color
            embeds.set_footer(text=embed_footer_text , icon_url= embed_footer_img)
            embeds.timestamp=datetime.datetime.utcnow()
            
            await ctx.send(embed = embeds)
        except:
            await ctx.send("Please try Again")
    @commands.command()
    async def stats(self , ctx):
        try:
            stats = get_stats(self.cName)
            #img = 'https://images-ext-2.discordapp.net/external/rJ1wqkAHV2IksRbZ-MtmR0z5D3tCnCkEkErms6_fuzk/https/lh3.googleusercontent.com/tjxKn8bHK9V6z-Fz8C8NBm3prH32f5BJso68m4hfQ9hp8FsFQyaYWTf4tcmouOorsttVNwOG7MWwaIi2yUAd2BDwIrbA4PvWSOt7qj8'
            embeds = discord.Embed()
            embeds.add_field(
                name='Average Price',
                value=str(stats['average_price']) + ' ' + emoji_id,
                inline=False
            )
            embeds.add_field(
                name='Holders',
                value=str(stats['num_owners']),
                inline=False
            )
            embeds.add_field(
                name='Total Supply',
                value=str(stats['total_supply']),
                inline=False
            )
            
            one_day_volume = "{:.2f}".format(stats['one_day_volume'])
            seven_Day_Volume = "{:.2f}".format(stats['seven_day_volume'])
            thirty_Day_Volume = "{:.2f}".format(stats['thirty_day_volume'])
            all_Time_Volume = "{:.2f}".format(stats['total_volume'])

            embeds.add_field(
                name='Volume \n',
                value=f'24 Hour Volume : {one_day_volume} {emoji_id}\n \nSeven Day Volume : {seven_Day_Volume} {emoji_id}\n \nThirty Day Volume : {thirty_Day_Volume} {emoji_id}\n \nAll time Volume : {all_Time_Volume} {emoji_id}\n',
                inline=False
            )
            embeds.color = embed_color
            embeds.set_footer(text=embed_footer_text , icon_url= embed_footer_img)
            embeds.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed = embeds)
        except:
            await ctx.send("Please try Again")
def setup(bot):
    bot.add_cog(OpenSeaBot(bot))

def parse_traits(traits,token,img,counts):
    embeds = discord.Embed(
        title = '#'+str(token)
    
    )
    embeds.set_image(url=str(img))
    
    
    for i in traits:
        meth = (i['trait_count']/counts)*100
        meth = int(round(meth))
        #meth = i['trait_count']
        embeds.add_field(
            name=str(i['trait_type']),
            value=str(i['value']) + f"\n({meth}%)",
            inline=True
        )
    return embeds