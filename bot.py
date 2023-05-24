import discord
from discord.ext import commands
import asyncio
from roblox import Client
import random
import string
import time
from discord.ext import tasks
import datetime
from keep_alive import keep_alive
import openai
import aiohttp
import requests
keep_alive()


client = Client("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_E8A8763D7C392A924F465CB0C16ECA25C42C403284B6211D2AB0E9C592387BDE73B1027DE9A9EA8B5B3A279D6381115B73D977AE65C744F7193F65EB19CE8F7B75378584090A2238C76D6C245C72230FDE582160FA8E6FDA4FB8D42970AE481EBD33B8A90BC67B624F9E76AF369FFECCE8975B65FBF033DB428CAD6FC897EF290D83EB0F6F52094AFAF7C52F25018577E283C7028FF1C9ECF88106938B660F343CD515C23B3EA1B07226E30E7AD6B365BC4DED98019F2FC45F6C5A75DD6BE3BDBF26C382AEC3CFCB688FCA1EBF8C9D50D73D858CAD7FEFE5D74973D82A44F0F985DFFB895CBF6041547933964BE386BB6A935669B5C2007255ECD7C95E7C4378B54D1EBA34ACBAE5BE096E960DAC159A6DDDE4AECA5A0230E7D8EAB9CD86A7E28BFAAC8AF46A817F6B8DB8A43D10F2B1C2EA3D6ECC6479EC6CF7367A74C18A155E40C233E44419596F1AF3C7CA31D79AF1944B3C242EE8DE08BFDE710D487B2A0E6652C5866A6CE5B305D3E7DB80C891EDF0C6E0")

API_KEY = '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'


@tasks.loop(minutes=1)
async def update_member_count():
    guild = bot.get_guild(1006829872963915796)  # Replace GUILD_ID with the ID of your guild
    channel = guild.get_channel(1110021505980583956)  # Replace CHANNEL_ID with the ID of the channel you want to rename
    
    member_count = len(guild.members)
    new_name = f"Members: {member_count}"
    
    await channel.edit(name=new_name)

async def main():
    await client.get_user(1)
    user = await client.get_authenticated_user()
    print("ID:", user.id)
    print("Name:", user.name)

asyncio.get_event_loop().run_until_complete(main())

class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=CustomHelpCommand())
bot.remove_command('help')


bot.remove_command('help')

MODERATOR_ROLE_IDS = [1110314708038324255, 1009736238477103134, 1009822264428085309, 1009828153633550416]

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="MiRBX | !help")
    await bot.change_presence(activity=activity)
    print(f"Logged in as {bot.user.name}")
    print("Bot is ready!")
    update_member_count.start()
    keep_alive()



@bot.event
async def on_member_join(member):
    # Get the channel where you want to send the message
    channel = bot.get_channel(1109943295137828996)  # Replace YOUR_CHANNEL_ID with the actual channel ID

    # Access the user object through the guild's member list
    user = member.guild.get_member(member.id)

    # Create an embed with the user's profile picture and information
    embed = discord.Embed(title="Welcome!", description=f"Welcome {member.mention} to the server!", color=discord.Color.green())
    embed.set_thumbnail(url=member.default_avatar)  # Access the avatar_url through user
    embed.add_field(name="Username", value=member.display_name, inline=True)  # Use display_name instead of name
    embed.add_field(name="Member Count", value=len(member.guild.members), inline=True)

    # Send the embed message to the channel
    await channel.send(embed=embed)

    # Add the role to the member
    role = discord.utils.get(member.guild.roles, name="Member")  # Replace "Your Role Name" with the actual role name
    await member.add_roles(role)


@bot.command()
@commands.has_any_role(*MODERATOR_ROLE_IDS)
async def mute(ctx, member: commands.MemberConverter=None, duration: str=None):
    if not member:
        error_embed = discord.Embed(title="Member Mute",
                                    description="Please mention a member to mute.",
                                    color=discord.Color.red())
        await ctx.send(embed=error_embed)
        return

    # If no duration is provided, show an error message
    if not duration:
        error_embed = discord.Embed(title="Member Mute",
                                    description="Please specify a duration for the mute.",
                                    color=discord.Color.red())
        await ctx.send(embed=error_embed)
        return

    # Parse the duration string to extract the numeric value and unit
    numeric_value = int(duration[:-1])
    time_unit = duration[-1].lower()

    # Convert the duration to seconds
    if time_unit == 'm':
        duration_seconds = numeric_value * 60
    elif time_unit == 'h':
        duration_seconds = numeric_value * 3600
    else:
        error_embed = discord.Embed(title="Member Mute",
                                    description="Invalid duration format. Please use 'm' for minutes or 'h' for hours.",
                                    color=discord.Color.red())
        await ctx.send(embed=error_embed)
        return
    
    # Mute the member
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(muted_role)

    # Send an embedded DM to the muted member
    dm_embed = discord.Embed(title="You have been muted",
                             description=f"You have been muted in {ctx.guild.name} for {numeric_value} {time_unit}.",
                             color=discord.Color.red())
    await member.send(embed=dm_embed)

    # Send an embedded log message to the specified channel
    log_channel = bot.get_channel(1006842020888850442)
    log_embed = discord.Embed(title="Member Muted",
                              description=f"{member.mention} has been muted for {numeric_value} {time_unit} by {ctx.author.mention}.",
                              color=discord.Color.red())
    await log_channel.send(embed=log_embed)

    # Send a message in the channel where the command was executed
    response_embed = discord.Embed(title="Member Muted",
                                   description=f"{member.mention} has been muted for {numeric_value} {time_unit}.",
                                   color=discord.Color.red())
    await ctx.send(embed=response_embed)

    # Wait for the mute duration and remove the muted role
    await asyncio.sleep(duration_seconds)
    await member.remove_roles(muted_role)


@bot.command()
async def gpt(ctx: commands.Context, *, prompt: str):
    async with aiohttp.ClientSession() as session:
        payload = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 50,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "best_of": 1,
        }
        headers = {"Authorization": f"Bearer {API_KEY}"}
        async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
            response = await resp.json()
            embed = discord.Embed(title="Chat GPT", description=response["choices"][0]["text"])
            await ctx.reply(embed=embed)

@bot.command()
@commands.has_any_role(*MODERATOR_ROLE_IDS)
async def ban(ctx, member: commands.MemberConverter=None, days: int=0):
    if not member:
        error_embed = discord.Embed(title="Ban Member",
                                    description="Please mention a member to ban.",
                                    color=discord.Color.red())
        await ctx.send(embed=error_embed)
        return

    if days <= 0:
        # Permanent ban
        await member.ban(reason="Permanently banned")
        ban_embed = discord.Embed(title="Member Banned",
                                  description=f"{member.mention} has been permanently banned.",
                                  color=discord.Color.red())
        await ctx.send(embed=ban_embed)
    else:
        # Temporary ban
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=days)
        unban_date = now + delta

        await member.ban(reason=f"Banned for {days} day(s)")
        ban_embed = discord.Embed(title="Member Banned",
                                  description=f"{member.mention} has been banned for {days} day(s).\n"
                                              f"They will be unbanned on {unban_date.strftime('%Y-%m-%d %H:%M:%S')}.",
                                  color=discord.Color.red())
        await ctx.send(embed=ban_embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):

     embed = discord.Embed(title="Bot Commands", description="List of available commands", color=discord.Color.blue())

     embed.add_field(name="!ping", value="Ping the bot.", inline=False)
     embed.add_field(name="!ban", value="Ban a member. (staff only)", inline=False)
     embed.add_field(name="!mute", value="Mute a member. (staff only)", inline=False)
     embed.add_field(name="!unmute", value="Unmute a member. (staff only)", inline=False)
     embed.add_field(name="!verify (DOWN)", value="Verify yourself (only available in verification channel).", inline=False)
     embed.add_field(name="!deverify (DOWN)", value="Deverify yourself.", inline=False)
     embed.add_field(name="!unban", value="Unban a member. (staff only)", inline=False)

     await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role(*MODERATOR_ROLE_IDS)
async def unban(ctx, member_id: int=None):
    if not member_id:
        await ctx.send("Please provide the ID of the member to unban.")
        return

    banned_users = await ctx.guild.bans()
    member = discord.utils.find(lambda u: u.user.id == member_id, banned_users)

    if not member:
        await ctx.send("The specified member is not banned.")
        return

    await ctx.guild.unban(member.user)
    unban_embed = discord.Embed(title="Member Unbanned",
                                description=f"{member.user.name}#{member.user.discriminator} has been unbanned.",
                                color=discord.Color.green())
    await ctx.send(embed=unban_embed)

@bot.command()
@commands.has_any_role(*MODERATOR_ROLE_IDS)
async def unmute(ctx, member: commands.MemberConverter=None):
    if not member:
        error_embed = discord.Embed(title="Unmuting",
                                    description="Please mention a member to unmute.",
                                    color=discord.Color.red())
        await ctx.send(embed=error_embed)
        return

    # Find the muted role
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("Muted role not found.")
        return

    # Check if the member has the muted role
    if muted_role not in member.roles:
        await ctx.send("The specified member is not muted.")
        return

    # Remove the muted role from the member
    await member.remove_roles(muted_role)

    # Send a success message
    success_embed = discord.Embed(title="Member Unmuted",
                                  description=f"{member.mention} has been unmuted.",
                                  color=discord.Color.green())
    await ctx.send(embed=success_embed)


@bot.command()
async def ping(ctx):
    start_time = time.time()
    message = await ctx.send("Pinging...")
    end_time = time.time()
    latency = (end_time - start_time) * 1000

    embed = discord.Embed(title="Pong!", color=discord.Color.green())
    embed.add_field(name="Latency", value=f"```{latency:.2f}ms```", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author.name}")

    await message.edit(content=None, embed=embed)

@update_member_count.before_loop
async def before_update_member_count():
    await bot.wait_until_ready()

@update_member_count.after_loop
async def after_update_member_count():
    if update_member_count.failed():
        # Handle any error that occurred during the task execution
        print("An error occurred during the member count update task.")

# Start the background task

@bot.command()
async def deverify(ctx):
    role_id = 1009735983564066826  # Replace with the ID of the role to be removed
    role = discord.utils.get(ctx.guild.roles, id=role_id)
    if role is None:
        embed = discord.Embed(title="Deverification", color=discord.Color.red())
        embed.add_field(name="Error", value="Role not found.", inline=False)
        await ctx.send(embed=embed)
        return

    if role not in ctx.author.roles:
        embed = discord.Embed(title="Deverification", color=discord.Color.red())
        embed.add_field(name="Error", value="You do not have the required role to be deverified.", inline=False)
        await ctx.send(embed=embed)
        return

    try:
        await ctx.author.remove_roles(role)
        embed = discord.Embed(title="Deverification", color=discord.Color.green())
        embed.add_field(name="Success", value="Role removed successfully.", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Deverification", color=discord.Color.red())
        embed.add_field(name="Error", value=f"Failed to remove role. Error: {str(e)}", inline=False)
        await ctx.send(embed=embed)


@bot.command()
async def verify(ctx, username):
    # Check if the command is used in the allowed channel
    allowed_channel_id = 1055217878741303347  # Replace with the ID of the allowed channel
    if ctx.channel.id != allowed_channel_id:
        embed = discord.Embed(title="Verification", color=discord.Color.red())
        embed.add_field(name="Error", value="This command can only be used in the allowed channel.", inline=False)
        embed.set_footer(text="To deverify, use the command !deverify.")
        await ctx.send(embed=embed)
        return

    # Generate a random string of letters
    random_letters = ''.join(random.choices(string.ascii_letters, k=10))

    embed = discord.Embed(title="Roblox Verification", color=discord.Color.blue())
    embed.add_field(name="Instructions", value=f"You have 3 minutes to put the following letters in your Roblox About Me: ```{random_letters}```", inline=False)
    embed.add_field(name="Verification", value="React with ✅ to verify.", inline=False)

    # Send the verification instructions
    verification_message = await ctx.send(embed=embed)
    await verification_message.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅"

    try:
        # Wait for the user to react with ✅
        reaction, _ = await bot.wait_for("reaction_add", timeout=180.0, check=check)
    except asyncio.TimeoutError:
        embed = discord.Embed(title="Verification", color=discord.Color.red())
        embed.add_field(name="Timeout", value="Verification timed out.", inline=False)
        await ctx.send(embed=embed)
        return

    # Retrieve the user's Roblox About Me
    try:
        user = await client.get_user_by_username(username)
        user_about_me = user.description
    except Exception as e:
        embed = discord.Embed(title="Verification", color=discord.Color.red())
        embed.add_field(name="Error", value=str(e), inline=False)
        await ctx.send(embed=embed)
        return

    # Check if the random letters are in the user's About Me
    if random_letters in user_about_me:
        embed = discord.Embed(title="Verification", color=discord.Color.green())
        embed.add_field(name="Success", value="Verification successful! You are now verified.", inline=False)
        await ctx.send(embed=embed)

        # Assign a role to the verified user
        role_id = 1009735983564066826  # Replace with the ID of the role you want to assign
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        await ctx.author.add_roles(role)
    else:
        embed = discord.Embed(title="Verification", color=discord.Color.red())
        embed.add_field(name="Failure", value="Verification failed. Please make sure the random letters are in your Roblox About Me.", inline=False)
        await ctx.send(embed=embed)


bot.run('MTEwOTk0NDMxNzczODQ4Nzk2OQ.GsCbpf.8ux5F0OZJLSQFm65IizgVO8JmEn8qZUDMTDzGA')
