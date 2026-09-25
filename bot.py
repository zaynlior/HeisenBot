import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import BadRequest

# ⚠️ SECURITY WARNING: Paste your NEW token here after revoking the leaked one in BotFather!
BOT_TOKEN = "YOUR_NEW_BOT_TOKEN_HERE"

REQUIRED_REFERRALS = 6
# 🔧 FIX: Channel usernames must include the '@' symbol. The bot MUST be an admin in this channel.
CHANNELS = ["@Heisenberg"]

# Database
conn = sqlite3.connect("referrals.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referrals INTEGER DEFAULT 0
)
""")
conn.commit()


async def check_channels(user_id, context):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except BadRequest:
            # 🔧 FIX: Handle cases where the user isn't found or the bot isn't an admin
            return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # 🔒 STEP 1 — Force channel join first
    joined = await check_channels(user_id, context)

    if not joined:
        keyboard = [
            [InlineKeyboardButton("🔗Join Heisen.city #Heisen", url="https://t.me/addlist/XgsEDHMz")],
            [InlineKeyboardButton("📢Join Operator: #Hesen", url="https://t.me/HeiseegO")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "⚠️ You must join the following channels to claim rewards:\n\n"
            "Operator #Heisen\n\n"
            "Please join all channels and put #heisen in your name to claim the rewards!",
            reply_markup=reply_markup
        )
        return

    # 🔥 STEP 2 — Save user if new
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute("INSERT INTO users (user_id, referrals) VALUES (?, ?)", (user_id, 0))
        conn.commit()

        # Referral logic
        if context.args:
            try:
                referrer_id = int(context.args[0])
                if referrer_id != user_id:
                    cursor.execute(
                        "UPDATE users SET referrals = referrals + 1 WHERE user_id=?",
                        (referrer_id,)
                    )
                    conn.commit()
            except ValueError:
                pass

    # 🔥 STEP 3 — Get referral count
    cursor.execute("SELECT referrals FROM users WHERE user_id=?", (user_id,))
    referral_count = cursor.fetchone()[0]

    bot_username = (await context.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    # 🎁 Reward unlock
    if referral_count >= REQUIRED_REFERRALS:
        await update.message.reply_text(
            "✅ Congratulations!\n\n"
            "🎁 You completed 10 referrals.\n"
            "PM @HeisenbergActives with ss from this bot to claim your reward."
        )
        return

    # 📈 Show referral progress
    await update.message.reply_text(
        f"🔥 Referral Task Unlocked!\n\n"
        f"Invite {REQUIRED_REFERRALS} friends using your personal link below.\n\n"
        f"👥 Progress: {referral_count}/{REQUIRED_REFERRALS}\n\n"
        f"🔗 Your Link:\n{referral_link}"
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # 🔧 FIX: drop_pending_updates ignores old spammed /start commands from when the bot was frozen
    app.run_polling(drop_pending_updates=True)
