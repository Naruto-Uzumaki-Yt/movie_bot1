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

from database import *
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

START_PIC = "https://graph.org/file/0e77ba48a8b7a3b09296f-362372bee0d84fd217.jpg"

START_TEXT = (
    "🎬 Welcome To Movie Search Bot\n\n"
    "✨ Search your favourite movies instantly.\n"
    "📥 Fast movie delivery\n"
    "🎞 Multi quality support\n"
    "Updates : @Anime_UpdatesAU"
)

HELP_TEXT = (
    "🆘 Help Menu\n\n"
    "• Send movie name to search\n"
    "• Select movie from buttons\n"
    "• Bot sends movie instantly\n"
    "• Join updates channel for access"
)

ABOUT_TEXT = (
    "ℹ️ About Bot\n\n"
    "Name : AU_ZoroFilter_bot\n"
    "Library : Pyrogram\n"
    "Language : Python\n"
    "Database : MongoDB\n"
    "Server : @BotsServerDead l\n"
    "Updates: @Anime_UpdatesAU\n"
    "Developer : Mr_Mohammed_29"
)

OWNER_TEXT = (
    "👑 Owner Details\n\n"
    "📢 Channel : @Anime_UpdatesAU"
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

    # FORCE SUB CHECK

    join = await subscribed(
        client,
        user_id
    )

    # USER NOT JOINED

    if not join:

        buttons = InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "📢 Join Updates",
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

    # START MENU

    await message.reply_photo(

        photo=START_PIC,

        caption=START_TEXT,

        reply_markup=home_buttons()
    )
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
    & (filters.document | filters.video)
)
async def save_movie(client, message):

    media = message.document or message.video

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

    await add_movie(data)

    print(f"✅ Saved : {file_name}")

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
    & ~filters.command(["start"])
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

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    files = results[start:end]

    buttons = []

    for movie in files:

        buttons.append([
            InlineKeyboardButton(
                movie["file_name"][:50],
                callback_data=f"movie#{movie['file_id']}"
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

    imdb = get_imdb(query)

    caption = (
        f"🔎 Results For : {query}"
    )

    if imdb:

        caption = (
            f"🎬 {imdb['title']} ({imdb['year']})\n"
            f"⭐ IMDB : {imdb['rating']}\n"
            f"🎭 Genre : {imdb['genre']}"
        )

    if imdb and imdb["poster"] != "N/A":

        await message.reply_photo(
            imdb["poster"],
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    else:

        await message.reply_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# ---------------- CALLBACK ----------------

@app.on_callback_query()
async def callback(
    client,
    query
):

    data = query.data

    if data.startswith("movie#"):

        file_id = data.split("#")[1]

        movie = await movies.find_one({
            "file_id": file_id
        })

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

            protect_content=False
        )

        await query.answer()

        # AUTO DELETE

        await asyncio.sleep(600)

        try:
            await sent.delete()

        except:
            pass

    # ---------------- PAGINATION ----------------

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
                    callback_data=f"movie#{movie['file_id']}"
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

@app.on_message(
    filters.command("stats")
    & filters.user(ADMINS)
)
async def stats(
    client,
    message
):

    total_users = (
        await users.count_documents({})
    )

    total_movies = (
        await movies.count_documents({})
    )

    text = (
        f"📊 Bot Stats\n\n"
        f"👤 Users : {total_users}\n"
        f"🎬 Movies : {total_movies}"
    )

    await message.reply_text(text)

# ---------------- RUN ----------------

print("🎬 Movie Bot Started")

app.run()

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
