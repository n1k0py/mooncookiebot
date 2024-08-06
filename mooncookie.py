import discord
from discord.ext import commands
from discord.ui import Button, View, Select, Modal, InputText
import random
import traceback

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=['!', '?', '#', '$', '%'], intents=intents)

CHANNEL_ID = 1081513632543809607  # Replace with your channel ID
DM_TEXT = "Thank you for your order! \nWe will contact you soon as possible!"  # Replace with your DM text
BOT_OWNER_ID = 986603094756450314  # Replace with your Discord user ID
random_color = discord.Colour(random.randint(0, 0xFFFFFF))

class OrderModal(Modal):
    def __init__(self):
        super().__init__(title="Order Details")

        self.add_item(InputText(label="First Name", placeholder="Enter your first name", max_length=30))
        self.add_item(InputText(label="Last Name", placeholder="Enter your last name", max_length=30))
        self.add_item(InputText(label="Email", placeholder="Enter your email", max_length=50))
        self.add_item(InputText(label="Address", placeholder="Enter your address", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        first_name = self.children[0].value
        last_name = self.children[1].value
        email = self.children[2].value
        address = self.children[3].value
        
        # Check if email contains '@'
        if '@' not in email:
            await interaction.response.send_message("Invalid email address. Please include '@' in your email.", ephemeral=True)
            return

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"New Order:\nFirst Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nAddress: {address}\nBy: <@{interaction.user.id}>")
        
        try:
            await interaction.user.send(DM_TEXT)
        except discord.Forbidden:
            await interaction.response.send_message("Unable to send DM. Please ensure your DMs are open.", ephemeral=True)

        await interaction.response.send_message("Your order has been received!", ephemeral=True)

class CookieSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Mixed box of 10 cookies", description="6.99€", value="10"),
            discord.SelectOption(label="Mixed box of 15 cookies", description="8.99€", value="15"),
            discord.SelectOption(label="Mixed box of 25 cookies", description="14.99€", value="25")
        ]
        super().__init__(placeholder="Choose your cookie box", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(OrderModal())

class StartButton(Button):
    def __init__(self):
        super().__init__(label="Start", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        view = View()
        view.add_item(CookieSelect())
        await interaction.response.send_message("Please choose a cookie box:\n\n**We deliver only in Italy, Torino.**", view=view, ephemeral=True)

class MyView(View):
    def __init__(self):
        super().__init__()
        self.add_item(StartButton())

@bot.event
async def on_ready():
    channel = bot.get_channel(1270335104107151383)
    if channel:
        await channel.send("Click the button to start your order:", view=MyView())
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Mooncookie"))

@bot.slash_command(name="order", description="Order Cookies", guild_ids=[1270335103440261141, 1000754975103795250])
async def order_slash(ctx):
    try:
        await ctx.user.send("Let's Start!", view=MyView())
        await ctx.respond("Check your DMs!")
    except discord.Forbidden:
        await ctx.respond("Unable to send DM. Please ensure your DMs are open.")

@bot.command(name="order")
async def order(ctx):
    try:
        await ctx.author.send("Let's Start!", view=MyView())
        await ctx.send("Check your DMs!")
    except discord.Forbidden:
        await ctx.send("Unable to send DM. Please ensure your DMs are open.")

@bot.slash_command(name="ping", description="Ping Bot", guild_ids=[1270335103440261141, 1000754975103795250])
async def ping(ctx):
    latency = round(bot.latency * 1000)
    ms = f'{latency}ms'
    embed = discord.Embed(title='Hello ' + ctx.author.name, description=ms, color=random_color)
    await ctx.respond(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send("Something went wrong, please ask the owner to check the logs.")
    owner = bot.get_user(BOT_OWNER_ID)
    if owner:
        error_details = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        await owner.send(f"Error in command {ctx.command}:\n{error_details}")

@bot.event
async def on_application_command_error(ctx, error):
    await ctx.respond("Something went wrong, please ask the owner to check the logs.")
    owner = bot.get_user(BOT_OWNER_ID)
    if owner:
        error_details = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        await owner.send(f"Error in command {ctx.command}:\n{error_details}")

bot.run('MTI3MDM1MDA3NDQ1MDI4NDU3NQ.GkumqW.qubaLEzxIrno2Ofynlyn-PKrrFuFVHhxke31PE')
