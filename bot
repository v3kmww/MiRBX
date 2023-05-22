import discord
from discord.ext import commands
import asyncio
from roblox import Client
import random
import string
import time
from discord.ext import tasks
client = Client("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_E8A8763D7C392A924F465CB0C16ECA25C42C403284B6211D2AB0E9C592387BDE73B1027DE9A9EA8B5B3A279D6381115B73D977AE65C744F7193F65EB19CE8F7B75378584090A2238C76D6C245C72230FDE582160FA8E6FDA4FB8D42970AE481EBD33B8A90BC67B624F9E76AF369FFECCE8975B65FBF033DB428CAD6FC897EF290D83EB0F6F52094AFAF7C52F25018577E283C7028FF1C9ECF88106938B660F343CD515C23B3EA1B07226E30E7AD6B365BC4DED98019F2FC45F6C5A75DD6BE3BDBF26C382AEC3CFCB688FCA1EBF8C9D50D73D858CAD7FEFE5D74973D82A44F0F985DFFB895CBF6041547933964BE386BB6A935669B5C2007255ECD7C95E7C4378B54D1EBA34ACBAE5BE096E960DAC159A6DDDE4AECA5A0230E7D8EAB9CD86A7E28BFAAC8AF46A817F6B8DB8A43D10F2B1C2EA3D6ECC6479EC6CF7367A74C18A155E40C233E44419596F1AF3C7CA31D79AF1944B3C242EE8DE08BFDE710D487B2A0E6652C5866A6CE5B305D3E7DB80C891EDF0C6E0")

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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="MiRBX")
    await bot.change_presence(activity=activity)
    print(f"Logged in as {bot.user.name}")
    print("Bot is ready!")
    update_member_count.start()



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
async def ping(ctx):
    latency = round(bot.latency * 1000) # Convert latency to milliseconds and round it

    embed = discord.Embed(title="Pong!", description=f"Latency: {latency}ms", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def verify(ctx, username):


    try:
        user = await client.get_user_by_username(username)
    except Exception as e:
     embed = discord.Embed(title="Verification", color=discord.Color.red())
     embed.add_field(name="Error", value="User is not a valid account!", inline=False)

     await ctx.send(embed=embed)
     return

    # Generate a random string of letters
    random_letters = ''.join(random.choices(string.ascii_letters, k=10))


    embed = discord.Embed(title="Roblox Verification", color=discord.Color.blue())
    embed.add_field(name="Instructions", value=f"You have 3 minutes to put the following letters in your Roblox description: ```{random_letters}```", inline=False)
    embed.add_field(name="Verification", value="Click the button below to verify", inline=False)

    # Send the random letters to the user

    # Create a verification message with a verify button
    verification_message = await ctx.send(embed=embed)


    # Add a verify button to the message
    await verification_message.add_reaction("✅")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅"


    try:
        # Wait for the user to click the verify button
        reaction, _ = await bot.wait_for("reaction_add", timeout=180.0, check=check)
    except asyncio.TimeoutError:
     embed = discord.Embed(title="Verification", color=discord.Color.red())
     embed.add_field(name="Timeout", value="Verification timed out.", inline=False)

     await ctx.send(embed=embed)

     return

    # Retrieve the user's Roblox description
    try:
        user = await client.get_user_by_username(username)
        user_description = user.description
    except Exception as e:
        embed = discord.Embed(title="Verification", color=discord.Color.red())
        embed.add_field(name="Error", value=f"Failed to retrieve user's Roblox description. Error: {str(e)}", inline=False)
        await ctx.send(embed=embed)
        return

    # Check if the user's Roblox description matches the random letters
    if random_letters in user_description:
        # Assign a role to the member


        # Set the server nickname to the Roblox username
        await ctx.author.edit(nick=username)

        embed = discord.Embed(title="Verification", color=discord.Color.green())
        embed.add_field(name="Success", value="Verification successful! You have been assigned a role and your nickname has been updated.", inline=False)
        await ctx.send(embed=embed)
        time.sleep(1)
        role_id = 1009735983564066826  # Replace with the ID of the role you want to assign
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        await ctx.author.add_roles(role)
    else:
        embed = discord.Embed(title="Verification", color=discord.Color.red())
        embed.add_field(name="Failure", value="Verification failed. Please make sure the random letters are in your Roblox description.", inline=False)
        await ctx.send(embed=embed)



bot.run('MTEwOTk0NDMxNzczODQ4Nzk2OQ.Gc--dn.qwUi8SB_W5gaWzVpKX_FRxSHNijtoBKlCzqyog')
