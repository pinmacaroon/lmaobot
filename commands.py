import discord
import re
import requests
import os
import json

import utils
import economy

async def l_hello(message: discord.Message, args: list) -> None:
    await message.reply(
        f'hello there <@{message.author.id}>, im ready to do bot stuff'
    )
    return

async def l_get_pfp(message: discord.Message, args: list) -> None:
    if len(args) < 2:
        await message.reply(
            f'not enough arguments! see `l!help l!get_pfp`'
        )
        return
    member: discord.Member
    member = utils.get_member_from_mention_and_server(args[1], message.guild)
    if member is None:
        await message.reply(
            f'user was not found!'
        )
        return
    file_id = utils.get_uuid()
    open(f"./tmp/{file_id}", "xb").write(requests.get(
        url=member.avatar.url,
        stream=True
    ).content)
    await message.reply(
        content=f'<@{member.id}>\'s pfp',
        file=discord.File(fp=f"./tmp/{file_id}", filename='pfp.png')
    )
    os.remove(f"./tmp/{file_id}")
    return

async def l_bal(message: discord.Message, args: list) -> None:
    if len(args) == 1:
        wallet = economy.get_or_create_member_wallet(
            message.author, message.guild
        )
        await message.reply(
            f'you have **${wallet["funds"]}** in your wallet, with a bonus of **{wallet["multiplier"]}%** !'
        )
        return
    else:
        member = utils.get_member_from_mention_and_server(args[1], message.guild)
        if not member:
            await message.reply(
                f'{args[1]} is not a valid user!'
            )
            return
        wallet = economy.get_or_create_member_wallet(
            member,
            message.guild
        )
        await message.reply(
            f'<@{member.id}> has **${wallet["funds"]}** in their wallet, with a bonus of **{wallet["multiplier"]}%** !'
        )
        return

COMMANDS = {
    'l!hello': l_hello,
    'l!get_pfp': l_get_pfp,
    'l!bal': l_bal
}