# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from flask import Flask

from threading import Thread

from database import add_movie, add_user, add_chat, movies, users
from config import *

import requests
import asyncio

# ---------------- WEB ----------------

web = Flask(__name__)

@web.route("/")
def home():
    return "Movie Bot Running"


@web.route("/watch/<file_id>")
def watch(file_id):
    return f"Streaming Enabled : {file_id}"


def run_web():
    web.run(
        host="0.0.0.0",
        port=8080
    )


Thread(target=run_web).start()

# ---------------- BOT ----------------

app = Client(
    "MovieBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

PAGE_SIZE = 5

search_cache = {}

# ---------------- START CONFIG ----------------

START_PIC = "https://ibb.co/qYBwMDby"

START_TEXT = (
    "👋 Hello {mention}\n\n"

    "🎬 I Am A Powerful AutoFilter Movie Bot.\n\n"

    "🔎 Send Any Movie Name\n"
    "📥 Get Files Instantly\n"
    "⚡ Fast Search System\n"
    "🎞 Multi Quality Support\n\n"

    "📢 Updates : @Anime_UpdatesAU"
)

HELP_TEXT = (
    "🆘 HELP MENU\n\n"

    "🔎 Send movie name to search\n"
    "📥 Click buttons to get files\n"
    "⚡ Fast movie searching\n"
    "🎞 Supports movies & series\n"
    "🗑 Auto delete enabled\n\n"

    "📢 Updates : @Anime_UpdatesAU"
)

ABOUT_TEXT = (
    "ℹ️ ABOUT BOT\n\n"

    "🤖 Name : @AU_ZoroFilter_bot\n"
    "⚡ Library : Pyrogram\n"
    "🐍 Language : Python\n"
    "🗄 Database : MongoDB\n"
    "🌐 Server : @BotsServerDead\n"
    "📢 Updates : @Anime_UpdatesAU\n"
    "👑 Developer : @Mr_Mohammed_29"
)

OWNER_TEXT = (
    "👑 OWNER DETAILS\n\n"

    "👤 Owner : @Mr_Mohammed_29\n"
    "📢 Channel : @Anime_UpdatesAU\n"
    "💬 Support : @AU_Bot_Discussion"
)

# ---------------- BUTTONS ----------------

def home_buttons():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🆘 Help",
                callback_data="help"
            ),

            InlineKeyboardButton(
                "ℹ️ About",
                callback_data="about"
            )
        ],

        [
            InlineKeyboardButton(
                "👑 Owner",
                callback_data="owner"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 Updates",
                url="https://t.me/Anime_UpdatesAU"
            )
        ]
    ])

# ---------------- IMDB ----------------

def get_imdb(query):

    try:

        url = (
            f"http://www.omdbapi.com/"
            f"?t={query}"
            f"&apikey={OMDB_API}"
        )

        r = requests.get(url).json()

        if r.get("Response") == "True":

            return {
                "title": r.get("Title"),
                "year": r.get("Year"),
                "rating": r.get("imdbRating"),
                "genre": r.get("Genre"),
                "poster": r.get("Poster")
            }

    except:
        return None

# ---------------- START ----------------

@app.on_message(filters.command("start"))
async def start(client, message):

    await add_user(message.from_user.id)

    user_id = message.from_user.id

    # FORCE SUB

    join = await subscribed(
        client,
        user_id
    )

    if not join:

        buttons = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "📢 Join Updates Channel",
                    url="https://t.me/Anime_UpdatesAU"
                )
            ],

            [
                InlineKeyboardButton(
                    "🔄 Try Again",
                    callback_data="checksub"
                )
            ]

        ])

        return await message.reply_photo(

            photo=START_PIC,

            caption=(
                "⚠️ Join updates channel first "
                "to use this bot."
            ),

            reply_markup=buttons
        )

    # START BUTTONS

    buttons = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "➕ Add Me To Your Group ➕",
                url=f"https://t.me/{(await client.get_me()).username}?startgroup=true"
            )
        ],

        [
            InlineKeyboardButton(
                "🎬 Movie Group",
                url="https://t.me/Anime_UpdatesAU"
            )
        ],

        [
            InlineKeyboardButton(
                "🆘 Help",
                callback_data="help"
            ),

            InlineKeyboardButton(
                "ℹ️ About",
                callback_data="about"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 Join Updates Channel 📢",
                url="https://t.me/Anime_UpdatesAU"
            )
        ]

    ])

    # START MESSAGE

    text = START_TEXT.format(
        mention=message.from_user.mention
    )

    await message.reply_photo(

        photo=START_PIC,

        caption=text,

        reply_markup=buttons
    )

@app.on_message(filters.group)
async def track_group(client, message):
    await add_chat(message.chat.id)
    
# ---------------- HOME ----------------

@app.on_callback_query(filters.regex("home"))
async def home_callback(client, query):

    await query.message.edit_caption(
        caption=START_TEXT,
        reply_markup=home_buttons()
    )

# ---------------- HELP ----------------

@app.on_callback_query(filters.regex("help"))
async def help_callback(client, query):

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            )
        ]
    ])

    await query.message.edit_caption(
        caption=HELP_TEXT,
        reply_markup=buttons
    )

# ---------------- ABOUT ----------------

@app.on_callback_query(filters.regex("about"))
async def about_callback(client, query):

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            )
        ]
    ])

    await query.message.edit_caption(
        caption=ABOUT_TEXT,
        reply_markup=buttons
    )

# ---------------- OWNER ----------------

@app.on_callback_query(filters.regex("owner"))
async def owner_callback(client, query):

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home"
            )
        ]
    ])

    await query.message.edit_caption(
        caption=OWNER_TEXT,
        reply_markup=buttons
    )

#------------- CHECK SUB -------------#
@app.on_callback_query(
    filters.regex("checksub")
)
async def check_sub_callback(
    client,
    query
):

    user_id = query.from_user.id

    join = await subscribed(
        client,
        user_id
    )

    if not join:

        return await query.answer(
            "Join updates channel first.",
            show_alert=True
        )

    await query.message.edit_caption(

        caption=START_TEXT,

        reply_markup=home_buttons()
    )

    await query.answer(
        "✅ Subscription verified"
    )
    
# ---------------- SAVE MOVIES ----------------

@app.on_message(
    filters.channel
    & filters.chat(LOG_CHANNEL)
)
async def save_movie(client, message):

    media = None

    # DOCUMENT

    if message.document:
        media = message.document

    # VIDEO

    elif message.video:
        media = message.video

    if not media:
        return

    file_name = media.file_name

    if not file_name:
        file_name = "Movie"

    data = {

        "file_name": file_name,

        "file_id": media.file_id,

        "file_size": media.file_size

    }

    # SAVE TO DATABASE

    await add_movie(data)

    print(
        f"✅ Saved : {file_name}"
    )

# ---------------- FORCE SUB ----------------

async def subscribed(client, user_id):

    # OWNER BYPASS

    if user_id in ADMINS:
        return True

    try:

        member = await client.get_chat_member(
            f"@{FORCE_SUB}",
            user_id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:
            return True

    except:
        return False
# ---------------- SEARCH ----------------

@app.on_message(
    filters.private
    & filters.text
    & ~filters.command([
        "start",
        "stats"
    ])
)
async def search_movie(
    client,
    message
):

    join = await subscribed(
        client,
        message.from_user.id
    )

    if not join:

        btn = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 Join Updates",
                    url="https://t.me/Anime_UpdatesAU"
                )
            ]
        ])

        return await message.reply_text(
            "Join updates channel first.",
            reply_markup=btn
        )

    query = message.text.lower()

    results = []

    async for movie in movies.find({
        "file_name": {
            "$regex": query,
            "$options": "i"
        }
    }):

        results.append(movie)

    if not results:

        return await message.reply_text(
            "❌ No movies found."
        )

    search_cache[
        message.from_user.id
    ] = results

    await send_page(
        message,
        results,
        0,
        query
    )

# ---------------- SEND PAGE ----------------

async def send_page(
    message,
    results,
    page,
    query
):

    import math
    import time

    start_time = time.time()

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    files = results[start:end]

    buttons = []

    # TOP FILTER BUTTONS

    buttons.append([

        InlineKeyboardButton(
            "📦 Send All",
            callback_data="send_all"
        ),

        InlineKeyboardButton(
            "🌐 LANGUAGES",
            callback_data="languages"
        ),

        InlineKeyboardButton(
            "📅 YEARS",
            callback_data="years"
        )

    ])

    buttons.append([

        InlineKeyboardButton(
            "🎞 QUALITY",
            callback_data="quality"
        ),

        InlineKeyboardButton(
            "📺 EPISODES",
            callback_data="episodes"
        ),

        InlineKeyboardButton(
            "📚 SEASONS",
            callback_data="seasons"
        )

    ])

    # MOVIE BUTTONS

    for movie in files:

        size = movie.get(
            "file_size",
            0
        )

        # SIZE FORMAT

        if size > 1024 * 1024 * 1024:

            file_size = (
                f"{size / (1024*1024*1024):.2f} GB"
            )

        else:

            file_size = (
                f"{size / (1024*1024):.2f} MB"
            )

        text = (
            f"[{file_size}] "
            f"{movie['file_name'][:45]}"
        )

        buttons.append([
            InlineKeyboardButton(
                text,
                callback_data=f"movie#{str(movie['_id'])}"
            )
        ])

    # PAGINATION

    total_pages = math.ceil(
        len(results) / PAGE_SIZE
    )

    nav = []

    if page > 0:

        nav.append(
            InlineKeyboardButton(
                "⬅️ BACK",
                callback_data=f"page#{page-1}"
            )
        )

    nav.append(
        InlineKeyboardButton(
            f"{page+1}/{total_pages}",
            callback_data="pages"
        )
    )

    if end < len(results):

        nav.append(
            InlineKeyboardButton(
                "NEXT ➡️",
                callback_data=f"page#{page+1}"
            )
        )

    buttons.append(nav)

    # SEARCH TIME

    search_time = (
        round(
            time.time() - start_time,
            2
        )
    )

    # CAPTION

    caption = (

        f"🔎 THE RESULTS FOR ➥ {query}\n\n"

        f"🙋 REQUESTED BY ➥ "
        f"{message.from_user.mention}\n\n"

        f"⚡ RESULT SHOW IN ➥ "
        f"{search_time} SECONDS\n\n"

        f"⚠️ AFTER 10 MINUTES "
        f"THIS MESSAGE WILL BE "
        f"AUTOMATICALLY DELETED 🗑"
    )

    imdb = get_imdb(query)

    # IMDB POSTER

    if imdb and imdb["poster"] != "N/A":

        sent = await message.reply_photo(

            photo=imdb["poster"],

            caption=caption,

            reply_markup=InlineKeyboardMarkup(buttons)
        )

    else:

        sent = await message.reply_text(

            caption,

            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # AUTO DELETE SEARCH MESSAGE

    await asyncio.sleep(600)

    try:
        await sent.delete()

    except:
        pass

# ---------------- CALLBACK ----------------

if data == "refresh_stats":

    if query.from_user.id not in ADMINS:
        return await query.answer("Not allowed", show_alert=True)

    text = await get_stats_text()

    btn = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats")
        ]
    ])

    await query.message.edit_text(text, reply_markup=btn)

    await query.answer("Updated ✅")

@app.on_callback_query()
async def callback(
    client,
    query
):

    data = query.data

    if data.startswith("movie#"):

        from bson import ObjectId

        movie_id = data.split("#")[1]

        movie = await movies.find_one({
            "_id": ObjectId(movie_id)
        })

        if not movie:
            return await query.answer(
                "Movie not found",
                show_alert=True
            )

        file_id = movie["file_id"]

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 Updates",
                    url="https://t.me/Anime_UpdatesAU"
                )
            ]
        ])

        sent = await query.message.reply_cached_media(

            file_id=file_id,

            caption=(
                f"{movie['file_name']}\n\n"
                f"Channel : @Anime_UpdatesAU"
            ),

            reply_markup=buttons,
        )

        await query.answer()

        # AUTO DELETE

        await asyncio.sleep(600)

        try:
            await sent.delete()

        except:
            pass

    # ---------------- PAGINATION ----------------
    elif data == "pages":

        await query.answer(
            "📄 Page Navigation"
        )

    elif data == "send_all":

        await query.answer(
            "❌ Send All Not Added Yet",
            show_alert=True
        )

    elif data == "languages":

        await query.answer(
            "🌐 Language Filter Coming Soon",
            show_alert=True
        )

    elif data == "years":

        await query.answer(
            "📅 Year Filter Coming Soon",
            show_alert=True
        )

    elif data == "quality":

        await query.answer(
            "🎞 Quality Filter Coming Soon",
            show_alert=True
        )

    elif data == "episodes":

        await query.answer(
            "📺 Episode Filter Coming Soon",
            show_alert=True
        )

    elif data == "seasons":

        await query.answer(
            "📚 Season Filter Coming Soon",
            show_alert=True
        )
        
    elif data.startswith("page#"):

        page = int(
            data.split("#")[1]
        )

        results = search_cache.get(
            query.from_user.id
        )

        if not results:
            return

        start = page * PAGE_SIZE
        end = start + PAGE_SIZE

        files = results[start:end]

        buttons = []

        for movie in files:

            buttons.append([
                InlineKeyboardButton(
                    movie["file_name"][:50],
                    callback_data=f"movie#{str(movie['_id'])}"
                )
            ])

        nav = []

        if page > 0:

            nav.append(
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data=f"page#{page-1}"
                )
            )

        if end < len(results):

            nav.append(
                InlineKeyboardButton(
                    "Next ➡️",
                    callback_data=f"page#{page+1}"
                )
            )

        if nav:
            buttons.append(nav)

        await query.message.edit_reply_markup(
            InlineKeyboardMarkup(buttons)
        )

# ---------------- STATS ----------------

@app.on_message(filters.command("stats"))
async def stats(client, message):

    if message.from_user.id not in ADMINS:
        return

    text = await get_stats_text()

    btn = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats")
        ]
    ])

    await message.reply_text(text, reply_markup=btn)

#------------ BROADCAST --------------#

@app.on_message(filters.command("broadcast"))
async def broadcast(client, message):

    if message.from_user.id not in ADMINS:
        return

    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to broadcast.")

    msg = message.reply_to_message

    users_list = users.find({})

    sent = 0

    async for user in users_list:
        try:
            await msg.copy(user["_id"])
            sent += 1
        except:
            pass

    await message.reply_text(f"📢 Broadcast sent to {sent} users")

#------------- INFO USER -------------#

@app.on_message(filters.command("info"))
async def info(client, message):

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    text = f"""
👤 User Info

🆔 ID: {user.id}
👤 Name: {user.first_name}
📛 Username: @{user.username if user.username else 'None'}
"""

    await message.reply_text(text)

# ---------------- RUN ----------------

print("🎬 Movie Bot Started")

app.run()

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
