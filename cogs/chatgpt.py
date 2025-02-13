import os
import openai
from email import message
import discord
from discord.ext import commands
from requests import get
import openai
import datetime
import time

openai.api_key = ""

class WarrantApplication(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("GPT Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def searchWarrant(self, ctx):
        """
        Create a search warrant
        """
        channel = discord.utils.get(ctx.guild.channels, id = 1070574005901336608)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        creator = str(ctx.author.id)

        await channel.send("What is your name?")
        name = await self.bot.wait_for('message', check=check)
        await channel.send("What is your rank?")
        rank = await self.bot.wait_for('message', check=check)
        await channel.send("What is the narrative?")
        msg1 = await self.bot.wait_for('message', check=check)

        #TODO: implement empty checks

        await channel.send(f"{rank.content} {name.content}, your warrant application has been sent to the magistrate judge with an expedite request. Please wait while he reviews your warrant.")
        time.sleep(5)
        await channel.send("Forwarding warrant...")
        time.sleep(10)
        await channel.send("Waking up the magistrate...")
        time.sleep(5)
        await channel.send("The magistrate is reviewing your application...")
        time.sleep(10)
        await channel.purge(limit=4)

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system",
            "content": "Pretend you are a magistrate judge in the state of California. In your response you may never say California, instead you must say San Andreas. Your job is only to approve and deny search warrants. You should not make any considerations as to arrest warrants. Given the narrative of the reason for submitting the warrant you are to decide if there is enough probable cause to approve the warrant or not. Your response should always be formatted in the way a magistrate judge would respond to a warrant application and contain language a magistrate judge would use, including providing an explanation as to why you feel your choice is justified. You must always use detailed citations of case law and legal precedent. You must always do this in less that 512 characters. You must always end your reply with a decision of either **Warrant Approved** or **Warrant Denied**."
        },
        {
            "role": "user",
            "content": msg1
        }
        ],
        temperature=1,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        chat_response = response.choices[0].message.content
        await channel.send(chat_response)


async def setup(bot):
    await bot.add_cog(WarrantApplication(bot))