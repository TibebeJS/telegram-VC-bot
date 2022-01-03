from telethon import TelegramClient, events, functions
from telethon.tl.types import (
    TypeInputChannel,
    PeerChannel,
    PeerUser,
    ChannelParticipantCreator,
    ChannelParticipantAdmin,
)
from telethon.tl.functions.channels import GetParticipantRequest
from pytgcalls import GroupCallFactory
from asyncio import sleep
from random import randint
import urllib
from requests import get


import asyncio

from telethon.utils import get_peer

from sqlite import VoiceChatDatabase

from dotenv import load_dotenv
from os import getenv

load_dotenv()

api_id = int(getenv("API_ID"))
api_hash = getenv("API_HASH")

GROUP_ID = int(getenv("GROUP_ID"))  # GROUP you want to install the bot on
LOG_CHANNEL_ID = int(getenv(
    "LOG_CHANNEL_ID"
))  # Channel where the logs are going to be sent to

LOGGER_BOT_TOKEN = getenv("LOGGER_BOT_TOKEN")

vc_db = VoiceChatDatabase(getenv("DB_FILENAME", "vc.db"))


def send_msg(chat_id, text):
    url_req = f"https://api.telegram.org/bot{LOGGER_BOT_TOKEN}/sendMessage?"
    qs = urllib.parse.urlencode(
        {
            "parse_mode": "Markdown",
            "chat_id": chat_id,
            "text": text,
        }
    )
    #    print(qs)
    get(url_req + qs)


def getFormattedMessage(user, participants):
    return f"""\
{
    "#LEFT" if participants[0].left else
    (
        "#JOINED" if participants[0].just_joined else
        (
            "#GENERIC"
        )
    )
}:
**ID:** `{user.id}`
**Name:** [{
    ((user.first_name if user.first_name is not None else "") + (user.last_name if user.last_name is not None else "")).replace('*', '🍔*').replace('_', '🍔_').replace('`', '🍔`')
}](tg://user?id={user.id}) 
**Username:** {
    ("@"+user.username.replace('*', '🍔*').replace('_', '🍔_').replace('`', '🍔`') if user.username is not None else "`None`")
}
""".replace(
        "🍔", "\\"
    )


def getFormattedMessageForMute(user, admin, reason, muted):
    return f"""\
{
    "#MUTED" if muted else "#UNMUTED"
}:
**ID:** `{user.id}`
**Name:** [{
    ((user.first_name if user.first_name is not None else "") + (user.last_name if user.last_name is not None else "")).replace('*', '🍔*').replace('_', '🍔_').replace('`', '🍔`')
}](tg://user?id={user.id}) 
**Username:** {
    ("@"+user.username.replace('*', '🍔*').replace('_', '🍔_').replace('`', '🍔`') if user.username is not None else "`None`")
}
**Voice Admin:** [{
    ((admin.first_name if admin.first_name is not None else "") + (admin.last_name if admin.last_name is not None else "")).replace('*', '🍔*').replace('_', '🍔_').replace('`', '🍔`')
}](tg://user?id={admin.id}) ({
    ("@"+admin.username.replace('*', '🍔*').replace('_', '🍔_').replace('`', '🍔`') if admin.username is not None else "`None`")
})
**Reason:** {reason}
""".replace(
        "🍔", "\\"
    )


async def is_admin(group_id, user_id):
    participant = await client(
        GetParticipantRequest(channel=group_id, participant=user_id)
    )
    isadmin = type(participant.participant) == ChannelParticipantAdmin
    iscreator = type(participant.participant) == ChannelParticipantCreator

    return isadmin or iscreator


with TelegramClient(getenv("SESSION_NAME", "user"), api_id, api_hash) as client:

    @client.on(events.NewMessage(pattern="setup", outgoing=True))
    async def handler(event):
        await client.get_dialogs()
        await client.get_dialogs(folder=0)
        await client.get_dialogs(folder=1)

    @client.on(events.NewMessage(pattern=r"^[!/]vmute (\d+) ?(.+)?$"))
    async def handler(event):
        # await event.delete()

        if not await is_admin(GROUP_ID, event.message.from_id.user_id):
            return await event.reply("Only admins can execute the commands")

        target_id = int(event.pattern_match.group(1))
        reason = str(event.pattern_match.group(2))

        if vc_db.is_user_muted(target_id):
            return await event.reply("User is already muted")

        try:
            admin = (
                await client(
                    functions.users.GetFullUserRequest(id=event.message.from_id.user_id)
                )
            ).user
        except ValueError:
            await event.reply("something went wrong locating admin.")
            return

        try:
            target_user = (
                await client(functions.users.GetFullUserRequest(id=target_id))
            ).user
        except ValueError:
            await event.reply("target not found.")
            return

        muted_successfully = vc_db.mute_user(
            target_user.id,
            target_user.first_name
            + (target_user.last_name if target_user.last_name is not None else ""),
            admin.id,
            (admin.last_name if admin.last_name is not None else ""),
            reason,
        )

        if muted_successfully:
            msg = getFormattedMessageForMute(target_user, admin, reason, True)
            send_msg(LOG_CHANNEL_ID, msg)
            # await event.reply(f"muted {target_user.first_name + (target_user.last_name if target_user.last_name is not None else '')} - Reason: {reason}")
        else:
            await event.reply(
                f"something went wrong trying to mute {target_user.first_name + (target_user.last_name if target_user.last_name is not None else '')}"
            )

    @client.on(events.NewMessage(pattern=r"^[!/]vunmute (\d+) ?(.+)?$"))
    async def handler(event):
        # await event.delete()

        if not await is_admin(GROUP_ID, event.message.from_id.user_id):
            return await event.reply("Only admins can execute the commands")

        target_id = int(event.pattern_match.group(1))
        reason = str(event.pattern_match.group(2))

        if vc_db.is_user_unmuted(target_id):
            return await event.reply("User is already unmuted")

        try:
            admin = (
                await client(
                    functions.users.GetFullUserRequest(id=event.message.from_id.user_id)
                )
            ).user
        except ValueError:
            await event.reply("something went wrong locating admin.")
            return

        try:
            target_user = (
                await client(functions.users.GetFullUserRequest(id=target_id))
            ).user
        except ValueError:
            await event.reply("target not found.")
            return

        unmuted_successfully = vc_db.unmute_user(
            target_user.id,
            target_user.first_name
            + (target_user.last_name if target_user.last_name is not None else ""),
            admin.id,
            (admin.last_name if admin.last_name is not None else ""),
            reason,
        )

        if unmuted_successfully:
            # await event.reply(f"unmuted {target_user.first_name + (target_user.last_name if target_user.last_name is not None else '')} - Reason: {reason}")
            msg = getFormattedMessageForMute(target_user, admin, reason, False)
            send_msg(LOG_CHANNEL_ID, msg)
        else:
            await event.reply(
                f"something went wrong trying to unmute {target_user.first_name + (target_user.last_name if target_user.last_name is not None else '')}"
            )

    @client.on(events.NewMessage(pattern=r"^\.join-vc$", outgoing=True))
    async def handler(event):
        try:
            print("starting monitoring...")
            group_call_factory = GroupCallFactory(
                client, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON
            )
            group_call = group_call_factory.get_file_group_call()

            await event.delete()

            result = await group_call.start(GROUP_ID)
            while not group_call.is_connected:
                await asyncio.sleep(1)
            print(result)

            async def handler(grpcall, participants):
                peer = participants[0].peer
                if type(peer) is PeerChannel:
                    if not participants[0].muted:
                        print("muted channel", peer.channel_id)
                        await group_call.edit_group_call_member(peer, muted=True)

                elif type(peer) is PeerUser:
                    result = await client(
                        functions.users.GetFullUserRequest(id=peer.user_id)
                    )

                    user = result.user

                    is_interesting_event = (
                        participants[0].left or participants[0].just_joined
                    )

                    if is_interesting_event:
                        msg = getFormattedMessage(user, participants)
                        send_msg(LOG_CHANNEL_ID, msg)

                    if participants[0].just_joined:
                        if vc_db.is_user_muted(user.id):
                            await group_call.edit_group_call_member(peer, muted=True)
                        elif vc_db.is_user_unmuted(user.id):
                            await group_call.edit_group_call_member(peer, muted=False)

        except Exception as e:
            print(e.message)
            return await event.reply(str(e))
        group_call.on_participant_list_updated(handler)

    client.run_until_disconnected()
