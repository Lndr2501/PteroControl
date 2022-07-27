import os
import sqlite3
import nextcord
from nextcord.ext import commands
import config

intents = nextcord.Intents.default()
intents.members = True


class Embed(nextcord.Embed):
    # add arguments for ctx and interaction
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_footer(
            text=f"When you have Problems, contact Lndr#2501 on Discord")
        self.color = nextcord.Colour.green()


class Bot(commands.Bot):
    def __init__(
        self, command_prefix=..., help_command=..., intents=..., owner_id=..., **options
    ):
        super().__init__(
            command_prefix=command_prefix,
            help_command=help_command,
            intents=intents,
            owner_id=owner_id,
            **options,
        )

        self.dbconn: sqlite3.Connection = sqlite3.connect("./database.db")
        self.dbcursor: sqlite3.Cursor = self.dbconn.cursor()

        self.persistent_views_added = False

        for file in os.listdir("./extensions"):
            if file.endswith(".py"):
                name = file[:-3]

                self.load_extension(f"extensions.{name}")
            else:
                print(f"Skipping {file}")

    async def on_ready(self):
        # add all persistent views when bot is ready (if not already added)
        readytext = """
                        _       
    _ __ ___  __ _  __| |_   _ 
    | '__/ _ \/ _` |/ _` | | | |
    | | |  __/ (_| | (_| | |_| |
    |_|  \___|\__,_|\__,_|\__, |
                        |___/ 
    """
        print(readytext)
        print(f"Logged in as {self.user.name}")
        print(f"With ID: {self.user.id}")
        print(f"On {len(self.guilds)} servers")
        print(f"With {len(self.users)} users")
        # print("Coded by Lndr#2501 with help from KingMigDOR#0001")
        print("-----------------------------------------------")


bot = Bot(
    command_prefix=commands.when_mentioned,
    help_command=None,
    intents=intents,
    owner_id=config.OWNERID,
)


# bot.run(config.TOKEN)

bot.run(config.LABORTOKEN)
