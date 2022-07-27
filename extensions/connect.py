import asyncio

import requests
import config
import nextcord
import main
import os
import aioconsole
from nextcord.ext import commands
from main import Embed
import sqlite3

conn = sqlite3.connect("./database.db")
cursor = conn.cursor()


class CreateModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="Pterodactyl authorizieren",
        )

        self.apikey = nextcord.ui.TextInput(
            label="API-Key",
            placeholder="z.B: ptlc_l2ec3SC2y97xt0DKA0cgUOCC5uBxdPHPsqLuGeZbunR",
            required=True,
        )
        self.add_item(self.apikey)

    async def callback(self, interaction: nextcord.Interaction) -> None:

        result = requests.post(
            "https://thunderhost.eu/api/application/user",
        )

        cursor.execute(
            "INSERT INTO accounts (discord_id, api_key) VALUES (?, ?)", (interaction.user.id, self.apikey.value))
        conn.commit()

        embed = Embed(
            title="Erfolgreich authentifiziert",
            description="Du kannst nun den Bot nutzen",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class RemoveButton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Jetzt", style=nextcord.ButtonStyle.blurple)
    async def jetzt(self, button: nextcord.Button, interaction: nextcord.Interaction):
        cursor.execute(
            "DELETE FROM accounts WHERE discord_id = ?", (interaction.user.id,))
        conn.commit()

        embed = Embed(
            title="Erfolgreich deauthorisiert",
            description="Du kannst nun den Bot nicht mehr nutzen",
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class CreateButton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Jetzt", style=nextcord.ButtonStyle.blurple)
    async def jetzt(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(CreateModal())


class Connect(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    # Code here
    @ nextcord.slash_command(name="connection", description="〣⚫| Verbinde deinen Pterodactyl Account mit dem Bot.", guild_ids=[config.GUILD])
    async def connection(self, interaction: nextcord.Interaction):
        ...

    @connection.subcommand(name="create", description="〣⚫| Erstelle eine Verbindung zu deinem Pterodactyl Account.")
    async def create(self, interaction: nextcord.Interaction):
        data = cursor.execute(
            "SELECT * FROM accounts WHERE discord_id = ?", (interaction.user.id,)).fetchall()

        if data:
            embed = Embed(
                title="Fehler",
                # TODO: add the slash command mention
                description="Du hast bereits einen Account der mit dem Bot verbunden. Um ihn zu entfernen, nutze den Befehl ",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        tutvideo = nextcord.File(
            "./media/how_to_apikey.mp4", filename="how_to_apikey.mp4")
        await interaction.response.send_message(content=f"{interaction.user.mention}. Gleich benötigst du einen API-Token von Pterodactyl. Wenn du den Key hast drücke auf 'Jetzt'. \nAnleitung: ", file=tutvideo, view=CreateButton())

    @connection.subcommand(name="remove", description="〣⚫| Trenne die Verbindung zu deinem Pterodactyl Account.")
    async def remove(self, interaction: nextcord.Interaction):
        data = cursor.execute(
            "SELECT * FROM accounts WHERE discord_id = ?", (interaction.user.id,)).fetchall()

        if not data:
            embed = Embed(
                title="Fehler",
                # TODO: add the slash command mention
                description="Du hast keinen Account der mit dem Bot verbunden ist. Um einen hinzuzufügen, nutze den Befehl </connection create:1001771646933291068>",
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        tutvideo = nextcord.File(
            "./media/how_to_apikey.mp4", filename="how_to_apikey.mp4")
        await interaction.response.send_message(content=f"{interaction.user.mention}. Gleich benötigst du einen API-Token von Pterodactyl. Wenn du den Key hast drücke auf 'Jetzt'", view=RemoveButton())


def setup(bot):
    bot.add_cog(Connect(bot))
