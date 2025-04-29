import sqlite3
import discord

def initialize_economy_for_server(server: discord.Guild) -> int:
    db = sqlite3.connect(f'./data/{str(server.id)}.db')
    cursor = db.cursor()
    try:
        cursor.executescript(open("./initecofs.sql", "r").read())
        db.commit()
    except sqlite3.OperationalError as e:
        pass
    db.close()
    return 0

def get_or_create_member_wallet(
        member: discord.Member, server: discord.Guild
    )-> object:
    db = sqlite3.connect(f'./data/{str(server.id)}.db')
    cursor = db.cursor()
    # TODO member's id should be embedded into the db cursor executions, but
    # sqlite3 is goofy and doesn't work
    member_id = member.id
    cursor.execute(
        open("./getmembwall.sql", "r").read(),
            (int(member_id),)
    )
    result: list = cursor.fetchall()
    if len(result) < 1:
        cursor.execute(
            open("./creamembwall.sql", "r").read(),
            (int(member_id),)
        )
        cursor.execute(
            open("./getmembwall.sql", "r").read(),
            (int(member_id),)
        )
        result: list = cursor.fetchall()
    db.commit()
    db.close()
    return {
        "id": result[0][0],
        "funds": result[0][1],
        "multiplier": result[0][2]
    }