# Importing Packages

from datetime import datetime
from discord.ext import commands, tasks
import discord
import os
import asyncio
from random import randint, choice
from discord.ext.commands import CheckFailure, has_role, has_permissions
from discord.utils import get
import requests
import json

# Creation & Configuration

bot = commands.Bot(command_prefix='!' , description=None)
bot.remove_command("help")

# Variables

token = "NzM0NDk1NDg2NzIzMjI3NzYw.XxSiOg.3B_xKd3mkEOavNHMrXaMX0HN_04"
core_color = discord.Color.from_rgb(30, 144, 255)
mn_color = discord.Color.from_rgb(35, 35, 35)
debug_mode = False
meaxisnetwork_url = "https://meaxisnetwork.net/assets/images/square_logo.png"
announcement_channel = "announcements"

# Events

@bot.event
async def on_ready():
    print("Bot online!")
    print("Logged into " + bot.user.name + "#" + bot.user.discriminator + "!")
    bot.loop.create_task(status_change())
    bot.load_extension(f'extensions.dbl')

@bot.event
async def on_command_error(ctx, error):
	if debug_mode == True:
		await ctx.send(str(error))
	else:
		print(str(error))

# Status

async def status_change():
	while True:
		statusTable = ["with CORE", "CORE Games", "over CORE Support", "with MikeyCorporation", "to commands"]
		statusChosen = choice(statusTable)
		if statusChosen != "over CORE Support" and statusChosen != "to commands":
			await bot.change_presence(activity=discord.Game(name=statusChosen))
		elif statusChosen == "over CORE Support":
			await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=statusChosen))
		else:
			await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=statusChosen))
		await asyncio.sleep(10)


# Commands

@bot.command()
async def load(ctx, extension):
    extensionLowered = extension.lower()
    bot.load_extension(f'extensions.{extensionLowered}')
    embed = discord.Embed(title="Extension loaded!", description=f"{extensionLowered}.py was loaded.", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def support(ctx):
    embed = discord.Embed(title="Support", description="Support Server: https://discord.gg/YH8WQCT", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="Bot Invite", description="https://discord.com/api/oauth2/authorize?client_id=734495486723227760&permissions=8&scope=bot", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'extensions.{extension}')

@bot.command()
async def debug(ctx, arg1):
	if arg1 == "on":
		global debug_mode
		debug_mode = True
	else:
		debug_mode = False


# MeaxisNetwork Commands

@bot.command()
async def profile(ctx):
	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "username"}
	usernameRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	usernameJSON = usernameRequest.json()
	username = usernameJSON["message"]

	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "description"}
	descriptionRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	descriptionJSON = descriptionRequest.json()
	description = descriptionJSON["message"]
	descriptionFixed = description.replace("\r", "")

	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "profilepicture"}
	avatarRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	avatarJSON = avatarRequest.json()
	avatarURLSource = descriptionJSON["message"]
	avatarURLString = str(avatarURLSource)
	avatarURLFixed = avatarURLString.replace(r'\/','/')

	payload = {"discordid": ctx.author.id, "secret": "t6ovhm._7-ng9iry-1602428551-gy1pn37w.u06x8_q", "scope": "id"}
	accountIDRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/fromdiscord/", params=payload)
	accountIDJSON = accountIDRequest.json()
	AccountID = accountIDJSON["message"]

	embed = discord.Embed(title=username, color=mn_color)
	embed.add_field(name = "Description", value = description, inline = False)
	embed.add_field(name = "Account ID", value = AccountID, inline = False)
	embed.set_thumbnail(url=meaxisnetwork_url)
	await ctx.send(embed=embed)

@bot.command()
async def funfact(ctx):
	funfactRequest = requests.get("https://api.meaxisnetwork.net/v2/funfact/")
	funfactJSON = funfactRequest.json()
	funfact = funfactJSON["text"]
	funfactID = funfactJSON["id"]
	funfactAuthor = funfactJSON["author"]
	
	embed = discord.Embed(title=f"Funfact #{funfactID}", color=mn_color)
	embed.add_field(name = "Funfact:", value = funfact, inline = False)
	embed.add_field(name = "Author", value = funfactAuthor, inline = False)
	embed.set_thumbnail(url=meaxisnetwork_url)
	await ctx.send(embed=embed)

@bot.command()
async def leafy(ctx):
	leafyRequest = requests.get("https://api.meaxisnetwork.net/v2/leafy/")
	embed = discord.Embed(title=f"Leafy API Status", color=mn_color)
	embed.add_field(name = "Status:", value = leafyRequest.status_code, inline = False)
	embed.add_field(name = "Note:", value = "If the status is 200, then the leafy API is online.", inline = False)
	embed.set_thumbnail(url=meaxisnetwork_url)
	await ctx.send(embed=embed)
	return

@bot.command()
async def finduser(ctx, username):
	payload = {"username": username}
	usernameRequest = requests.get("https://api.meaxisnetwork.net/v2/accounts/exists/", params=payload)
	usernameJSON = usernameRequest.json()
	usernameResult = usernameJSON["message"]
	embed = discord.Embed(title="User Result", color=mn_color)
	embed.add_field(name = "Username Entered:", value = username, inline = False)
	embed.add_field(name = "Result:", value = usernameResult, inline = False)
	embed.set_thumbnail(url=meaxisnetwork_url)
	await ctx.send(embed=embed)

@bot.command()
async def run(ctx, *, cmd):
    if ctx.author.id == 635119023918415874:
        try:
            eval(cmd)
            await ctx.send(f'CORE executed your command --> {cmd}')
        except:
            print(f'{cmd} is an invalid command')
            await ctx.send(f'CORE could not execute an invalid command --> {cmd}')



@bot.command()
@has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    embed=discord.Embed(title="User muted!", description="**{0}** was muted by **{1}**!".format(member.display_name, ctx.author.name), color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def maths(ctx, arg="practise", arg2="add", arg3=5, arg4=91):
	if arg == "practise":
		num1 = randint(100, 1000)
		num2 = randint(1000, 5000)
		result = num1 + num2
		mathsEmbed = discord.Embed(title="Maths with CORE", description=f"Work out this calculation and say it in chat.\n\n{num1} + {num2}", color=core_color)
		mathsEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		await ctx.send(embed=mathsEmbed)
		msg = await bot.wait_for("message")
		if msg.content == str(result):
			succesfulEmbed = discord.Embed(title="Maths with CORE", description="You successfully guessed the answer.", color=core_color)
			succesfulEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=succesfulEmbed)
		else:
			failureEmbed = discord.Embed(title="Maths with CORE", description="Answer was incorrect.", color=core_color)
			failureEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=failureEmbed)
	elif arg == "operation":
		if arg2 == "add":
			number = arg3 + arg4
			addEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
			addEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=addEmbed)
		if arg2 == "minus" or arg2 == "subtract":
			number = arg3 - arg4
			subtractEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
			subtractEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=subtractEmbed)
		if arg2 == "multiply" or arg2 == "times":
			number = arg3 * arg4
			multiplyEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
			multiplyEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=multiplyEmbed)
		if arg2 == "divide" or arg2 == "share":
			number = arg3 / arg4
			divideEmbed = discord.Embed(title="Maths with CORE", description=f"Answer is: {number}", color=core_color)
			divideEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
			await ctx.send(embed=divideEmbed)

@bot.command()
@has_permissions(manage_messages=True) 
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role)
    embed=discord.Embed(title="User unmuted!", description="**{0}** was unmuted by **{1}**!".format(member.display_name, ctx.author.name), color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx, *, member: discord.Member):
    fmt = '{0} joined on {0.joined_at} and has {1} roles.'
    infoEmbed = discord.Embed(title="Information", description=fmt.format(member, len(member.roles)), color=core_color)
    infoEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=infoEmbed)

@bot.command()
async def rps(ctx, arg):
    embed = discord.Embed(title="Rock Paper Scissors!", color=core_color)
    if arg.lower() == "rock":
        embed.description = "Paper!"
    elif arg.lower() == "paper":
        embed.description = "Scissors!"
    elif arg.lower() == "scissors":
        embed.description = "Rock!"
    await ctx.send(embed=embed)

# Announcement Commands

@bot.command()
async def set(ctx,*,channel):
    global announcement_channel
    announcement_channel = channel
    embed = discord.Embed(title="Successfully Changed", description="The announcement channel has been changed.", color=core_color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(manage_channels=True) 
async def announce(ctx):
    channel = ctx.message.channel
    announcements = discord.utils.get(ctx.message.channel.guild.text_channels , name=announcement_channel)
    areSureEmbed = discord.Embed(title="Announcement" , description="What is the body of the announcement?" ,
                                 color=core_color)
    await ctx.send("" , embed=areSureEmbed)

    def check(m):
        return m.channel == channel and m.author == ctx.message.author

    try:
        msg = await bot.wait_for('message' , check=check , timeout=120)
        if msg.content == "cancel":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=core_color)
            await channel.send("" , embed=cancelEmbed)
            return
        CategoryEmbed = discord.Embed(title="Announcement" ,
                                                     description="What catgegory is your announcement? Categories: information, warning, important",
                                                     color=core_color)

        await channel.send(''.format(msg) , embed=CategoryEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=core_color)
        await channel.send("" , embed=TimeoutEmbed)

    def yesCheck(m):
        return m.channel == channel and m.author == ctx.message.author
    try:
        categoryMsg = await bot.wait_for('message' , check=check , timeout=120)
        if msg.content == "cancel":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=core_color)
            await channel.send("" , embed=cancelEmbed)
            return
        SendingAnnouncementEmbed = discord.Embed(title="Announcement" ,
                                                     description="Are you sure you want to send this announcement?\n\n" + msg.content ,
                                                     color=core_color)

        await channel.send(''.format(msg) , embed=SendingAnnouncementEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=core_color)
        await channel.send("" , embed=TimeoutEmbed)
    try:
        Message = await bot.wait_for('message' , check=yesCheck , timeout=120)
        if Message.content == "cancel" or Message.content == "no":
            cancelEmbed = discord.Embed(title="Announcement" , description="Successfully cancelled!" ,
                                            color=core_color)
            await channel.send("" , embed=cancelEmbed)
            return
        if categoryMsg.content == "placeholder":
            AnnouncementEmbed = discord.Embed(title="CORE | Information" , description=msg.content ,

                                              color=core_color)
            AnnouncementEmbed.set_thumbnail(
                url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-Logo_informations.png?width=468&height=468")

        elif categoryMsg.content == "information":
            AnnouncementEmbed = discord.Embed(title="CORE | Information" , description=msg.content ,

                                              color=discord.Color.from_rgb(0 , 0 , 255))
            AnnouncementEmbed.set_thumbnail(
                url="https://media.discordapp.net/attachments/733628287548653669/754109649074257960/768px-Logo_informations.png?width=468&height=468")

        elif categoryMsg.content == "important":
            AnnouncementEmbed = discord.Embed(title=":loudspeaker: Important Announcement" , description=msg.content ,

                                              color=discord.Color.from_rgb(255 , 0 , 0))
            AnnouncementEmbed.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/746034342303891585.png?v=1")
        elif categoryMsg.content == "warning":
            AnnouncementEmbed = discord.Embed(title=":warning: Warning Announcement" , description=msg.content ,

                                              color=discord.Color.from_rgb(252, 206, 0))
            await announcements.send("", embed=AnnouncementEmbed)
            return
        elif categoryMsg.content == "critical":
            if ctx.message.author.id == 635119023918415874:
                AnnouncementEmbed = discord.Embed(title=":no_entry_sign: | Critical Announcement" ,
                                                  description=msg.content ,

                                                  color=discord.Color.from_rgb(255 , 0 , 0))
            else:
                UnauthorisedUseOfCritical = discord.Embed(title=":no_entry_sign: You are unauthorised to use this category.", description="You are not authorised to use this category, please use another category, this category can only be used by the Bot Developer.", color= discord.Color.from_rgb(255, 0, 0))
                await ctx.send("", embed=UnauthorisedUseOfCritical)
                return
        elif categoryMsg.content == "developmentWithPing":
            if ctx.message.author.id == 635119023918415874:
                TestingEmbed = discord.Embed(title=":construction:  Development Announcement" ,
                                                  description=msg.content ,

                                                  color=discord.Color.from_rgb(255, 145, 0))
                await announcements.send("@everyone", embed=TestingEmbed)
                return
            else:
                PleaseTryAgain = discord.Embed(title="Error:" ,
                                               description="You did not put the one of the valid categories available for this announcement, please try again." ,
                                               color=discord.Color.from_rgb(255 , 0 , 0))
                await ctx.send("" , embed=PleaseTryAgain)
                return
        elif categoryMsg.content == "development":
            if ctx.message.author.id == 635119023918415874:
                TestingEmbed = discord.Embed(title=":construction:  Development Announcement" ,
                                             description=msg.content ,

                                             color=discord.Color.from_rgb(255 , 145 , 0))
                await announcements.send("" , embed=TestingEmbed)
                return
            else:
                PleaseTryAgain = discord.Embed(title="Error:" ,
                                               description="You did not put the one of the valid categories available for this announcement, please try again." ,
                                               color=discord.Color.from_rgb(255 , 0 , 0))
                await ctx.send("" , embed=PleaseTryAgain)
                return


        else:
            PleaseTryAgain = discord.Embed(title="Error:", description="You did not put the one of the valid categories available for this announcement, please try again.", color= discord.Color.from_rgb(255, 0, 0))
            await ctx.send("", embed=PleaseTryAgain)
            return
        SendingAnnouncementEmbed = discord.Embed(title="Announcement" ,
                                                     description="Sending announcement...\n\n" + msg.content ,
                                                     color=core_color)
        await channel.send(''.format(msg) , embed=SendingAnnouncementEmbed)
        await announcements.send("@everyone" , embed=AnnouncementEmbed)
    except asyncio.TimeoutError:
        TimeoutEmbed = discord.Embed(title="Timeout!" ,
                                         description="You have reached the 120 second timeout! Please send another command if you want to continue!" ,
                                         color=core_color)
        await channel.send("" , embed=TimeoutEmbed)

@bot.command()
@has_permissions(kick_members=True) 
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    kickEmbed = discord.Embed(title="Successfully Kicked.", description=member.display_name + " was kicked for: " + reason, color=core_color)
    if reason == None:
        kickEmbed.description = member.display_name + "was kicked successfully."
    await ctx.send(embed=kickEmbed)

@bot.command()
@has_permissions(ban_members=True) 
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    banEmbed = discord.Embed(title="Successfully Banned.", description=member.display_name + " was banned for: " + reason, color=core_color)
    if reason == None:
        banEmbed.description = member.display_name + "was banned successfully."
    await ctx.send(embed=banEmbed)


@bot.command()
async def categories(ctx):
    f = discord.Embed(title="Categories", description="These are the categories for the CORE Announce command:\n\ninformation,\nimportant,\nwarning", color=core_color)
    f.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=f)

def is_in_guild(guild_id):
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == guild_id
    return commands.check(predicate)

@bot.command()
@is_in_guild(722195079262896239)
@has_role("[-] 𝙎𝙩𝙖𝙛𝙛")
async def duty(ctx, arg1="On-Duty"):
	channel = discord.utils.get(ctx.message.channel.guild.text_channels , name="on-duty")
	embed = discord.Embed(title="Duty Changed", color=core_color)
	embed.add_field(name="Name", value=ctx.author.name, inline=True)
	if arg1.lower() == "off" or arg1 == "off-duty":
		embed.add_field(name="Status", value="Off-Duty", inline=True)
	else:
		embed.add_field(name="Status", value="On-Duty", inline=True)
	embed.add_field(name="Time", value=f"{datetime.utcnow()}")
	embed.set_thumbnail(url=str(ctx.message.author.avatar_url))
	await channel.send(embed=embed)

@bot.command()
@is_in_guild(722195079262896239)
async def verify(ctx):
	member = ctx.message.author
	role = get(member.guild.roles, name="[-] 𝙍𝙊𝘽𝙇𝙊𝙓𝙞𝙖𝙣𝙨")
	if role in member.roles:
		embed = discord.Embed(title="Verification", description="You are already verified. No roles have been added.", color=core_color)
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		await ctx.send(embed=embed)
	else:
		await member.add_roles(role)
		embed = discord.Embed(title="Verification", color=core_color)
		embed.add_field(name="Added Roles", value="[-] 𝙍𝙊𝘽𝙇𝙊𝙓𝙞𝙖𝙣𝙨")
		embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
		await ctx.send(embed=embed)




@bot.command()
async def random(ctx):
    randomMember = choice(ctx.guild.members)
    await ctx.send(f'{randomMember.mention} has been chosen.')

@bot.command()
async def help(ctx):
    helpEmbed = discord.Embed(color=core_color, title="CORE | Help")
    helpEmbed.set_footer(text="CORE | Help")
    helpEmbed.add_field(name="!help", value="Help Command for CORE", inline=False)
    helpEmbed.add_field(name="!rps", value="Rock Paper Scissors", inline=False)
    helpEmbed.add_field(name="!maths", value="A maths game where you need to work out the answer for a random calculation!", inline=False)
    helpEmbed.add_field(name="!random", value="Chooses a random user and says that they are the chosen one", inline=False)
    helpEmbed.add_field(name="!purge", value="To clear a selected amount of messages in that channel", inline=False)
    helpEmbed.add_field(name="!version", value="Specifies the most recent update for CORE", inline=False)
    helpEmbed.add_field(name="!kick", value="Kicks a user that you specify", inline=False)
    helpEmbed.add_field(name="!ban", value="Bans a user that you specify", inline=False)
    helpEmbed.add_field(name="!announce", value="Announces a message in the announcement channel", inline=False)
    helpEmbed.add_field(name="!load", value="Loads a specific extension", inline=False)
    helpEmbed.add_field(name="!unload", value="Unloads a specific extension", inline=False)
    helpEmbed.add_field(name="!categories", value="Specifies the available announcement categories", inline=False)
    helpEmbed.add_field(name="!info", value="Specifies information about a certain member", inline=False)
    helpEmbed.add_field(name="!support" ,value="Specifies the support server.", inline=False)
    helpEmbed.add_field(name="!invite", value="Allows you to invite the bot.", inline=False)
    helpEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=helpEmbed)

@bot.command()
async def version(ctx):
    updateEmbed = discord.Embed(title="Most recent version:", description="Version 1.0.6\n\n- Debug Mode\n\n      - Added a range of statuses for the bot to roll through.\n\n      - Properly established random command, useful for giveaways.\n", color=core_color)
    updateEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/734495486723227760/dfc1991dc3ea8ec0f7d4ac7440e559c3.png?size=128")
    await ctx.send(embed=updateEmbed)

@bot.command()
@has_permissions(manage_channels=True)
async def purge(ctx, amount=15):
    new_amount = amount + 1
    await ctx.channel.purge(limit=new_amount)

bot.run(token)
