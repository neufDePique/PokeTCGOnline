from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_ADMIN_USER_IDS
from src.services.localization_service import LocalizationService
from src.services.settings_service import SettingsService
from src.services.user_service import UserService


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot, settings_service: SettingsService,
                 localization_service: LocalizationService, user_service: UserService) -> None:
        self.bot = bot
        self.settings_service = settings_service
        self.t = localization_service.get_string
        self.user_service = user_service

    @app_commands.command(name="give_money", description="Give or take money to the user")
    async def give_money_command(self, interaction: discord.Interaction, member: discord.User, money: int) -> None:
        user_language_id = self.settings_service.get_user_language_id(interaction.user)

        if interaction.user.id not in BOT_ADMIN_USER_IDS:
            await interaction.response.send_message(self.t(user_language_id, 'common.not_allowed'))
            return

        if self.user_service.give_money(member.id, money):
            await interaction.response.send_message(
                self.t(user_language_id, 'give_money_cmd.response_msg').format(user=f"{member.id} ({member.name})",
                                                                               amount=money))
        else:
            await interaction.response.send_message(
                self.t(user_language_id, 'common.user_not_found'))

    @app_commands.command(name="give_all_money", description="Give or take money to every users")
    async def give_all_money_command(self, interaction: discord.Interaction, money: int) -> None:
        user_language_id = self.settings_service.get_user_language_id(interaction.user)

        if interaction.user.id not in BOT_ADMIN_USER_IDS:
            await interaction.response.send_message(self.t(user_language_id, 'common.not_allowed'))
            return

        if self.user_service.give_all_money(money):
            await interaction.response.send_message(
                self.t(user_language_id, 'give_all_money_cmd.response_msg').format(amount=money))
        else:
            await interaction.response.send_message(
                self.t(user_language_id, 'common.unknown_issue'))

    @app_commands.command(name="give_card", description="Give a card to the user")
    async def give_card_command(self, interaction: discord.Interaction, member: discord.User, card_id: str) -> None:
        user_language_id = self.settings_service.get_user_language_id(interaction.user)

        if interaction.user.id not in BOT_ADMIN_USER_IDS:
            await interaction.response.send_message(self.t(user_language_id, 'common.not_allowed'))
            return

        if self.user_service.add_cards_to_collection(member.id, [card_id]):
            await interaction.response.send_message(
                self.t(user_language_id, 'give_card_cmd.response_msg').format(user=f"{member.id} ({member.name})",
                                                                              card_id=card_id))
        else:
            await interaction.response.send_message(
                self.t(user_language_id, 'common.user_not_found'))

    @app_commands.command(name="remove_card", description="Remove a card from the user")
    async def remove_card_command(self, interaction: discord.Interaction, member: discord.User, card_id: str) -> None:
        user_language_id = self.settings_service.get_user_language_id(interaction.user)

        if interaction.user.id not in BOT_ADMIN_USER_IDS:
            await interaction.response.send_message(self.t(user_language_id, 'common.not_allowed'))
            return

        if self.user_service.remove_card_from_collection(member.id, card_id):
            await interaction.response.send_message(
                self.t(user_language_id, 'remove_card_cmd.response_msg').format(user=f"{member.id} ({member.name})",
                                                                                card_id=card_id))
        else:
            await interaction.response.send_message(
                self.t(user_language_id, 'common.user_or_card_not_found'))

    @app_commands.command(name="give_boosters", description="Give some boosters to the user")
    async def give_boosters_command(self, interaction: discord.Interaction, member: discord.User,
                                    kind: Literal["Basic", "Promo"],
                                    quantity: int) -> None:
        user_language_id = self.settings_service.get_user_language_id(interaction.user)

        if interaction.user.id not in BOT_ADMIN_USER_IDS:
            await interaction.response.send_message(self.t(user_language_id, 'common.not_allowed'))
            return

        if self.user_service.give_boosters(member.id, kind, quantity):
            await interaction.response.send_message(
                self.t(user_language_id, 'give_boosters_cmd.response_msg').format(user=f"{member.id} ({member.name})",
                                                                                  kind=kind, quantity=quantity))
        else:
            await interaction.response.send_message(
                self.t(user_language_id, 'common.user_not_found'))

    @app_commands.command(name="give_all_boosters", description="Give some boosters to every users")
    async def give_all_boosters_command(self, interaction: discord.Interaction,
                                        kind: Literal["Basic", "Promo"],
                                        quantity: int) -> None:
        user_language_id = self.settings_service.get_user_language_id(interaction.user)

        if interaction.user.id not in BOT_ADMIN_USER_IDS:
            await interaction.response.send_message(self.t(user_language_id, 'common.not_allowed'))
            return

        if self.user_service.give_all_boosters(kind, quantity):
            await interaction.response.send_message(
                self.t(user_language_id, 'give_all_boosters_cmd.response_msg').format(kind=kind, quantity=quantity))
        else:
            await interaction.response.send_message(
                self.t(user_language_id, 'common.unknown_issue'))
