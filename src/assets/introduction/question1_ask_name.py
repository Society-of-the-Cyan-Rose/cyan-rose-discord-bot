from discord.ui import Button, View, Modal, TextInput, button
from discord import Embed, ButtonStyle, Interaction
from database.tables import Introduction

from . import question2_ask_birth

import logging

logger = logging.getLogger("cyan")

name_embed = Embed(title="What's your name?", 
                   description=(
                     "Tell me what name, nickname, or alias you want"
                     "to be called in the Society."
                   ),
                   color=0x00ffff,)
name_embed.set_thumbnail(url="https://raw.githubusercontent.com/Society-of-the-Cyan-Rose/cyan-rose-discord-bot/main/src/assets/cyan-rose.png")

class name_modal(Modal):
    def __init__(self):
        super().__init__(timeout=None, title="What's your name?")

        self.name_input = TextInput(label="Name(s), Nickname(s), or Alias:", placeholder="Ron Swanson", min_length=2, max_length=50, required=True)
        self.add_item(self.name_input)
    
    async def interaction_check(self, interaction: Interaction):

        if Introduction.select().where(Introduction.user_id == interaction.user.id, Introduction.part == 0).exists():
            Introduction.update(introduction=self.name_input.value).where(Introduction.user_id == interaction.user.id, Introduction.part == 0).execute()
            logger.debug(f"Updated name for user: {interaction.user}")
        else:
            Introduction.create(user_id=interaction.user.id, part=0, introduction=self.name_input.value)
            logger.debug(f"Created name for user: {interaction.user}")
        logger.debug(f"Passing to: question2_ask_birth")
        await interaction.response.edit_message(embed=question2_ask_birth.birth_embed, view=question2_ask_birth.birth_view())

class name_view(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="you can call me...", style=ButtonStyle.primary)
    async def get_name_button(self, interaction : Interaction, button : Button):
        logger.debug(f"Button: Get Name - question1 - introduction | User: {interaction.user}")
        await interaction.response.send_modal(name_modal())
