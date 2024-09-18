import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
WEBPAGE_URL = 'http://localhost:5000/verify' # a recupérer manuellement

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')

class RoleView(View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.add_item(Button(label="Vérifier et obtenir le rôle", style=nextcord.ButtonStyle.link, url=f"{WEBPAGE_URL}?id={self.user_id}"))

@bot.command()
async def grole(ctx):
    view = RoleView(ctx.author.id)

    embed = nextcord.Embed(
        title="Vérification de Rôle",
        description="Cliquez sur le bouton ci-dessous pour vérifier votre compte et obtenir un rôle sur notre serveur Discord.",
        color=0x000000
    )
    
    await ctx.author.send(
        embed=embed,
        view=view
    )

bot.run('token') # token de ton bot
