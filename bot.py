import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔥 PASTE YOUR BOT TOKEN HERE
BOT_TOKEN = "8726690172:AAHR-uEgB4E8sGkD6YXgUxAGlAa0HNXTptA"

REQUIRED_REFERRALS = 20
CHANNELS = ["@HeisenOperator"]

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
        member = await context.bot.get_chat_member(channel, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # 🔒 STEP 1 — Force channel join first
    joined = await check_channels(user_id, context)

    if not joined:
        keyboard = [
            [InlineKeyboardButton("🔗Join Heisen.city #Heisen", url="https://t.me/addlist/Hztgg24Yyjc0YmUx")],
            [InlineKeyboardButton("📢Join Operator: #Heisen", url="https://t.me/HeisenOperator")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "⚠️ You must join all channels first to unlock your referral task.\n\n"
            "After joining, press /start again.",
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
            except:
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
            "🎁 You completed 20 referrals.\n"
            "PM @HeisenbergActives to claim your reward."
        )
        return

    # 📈 Show referral progress
    await update.message.reply_text(
        f"🔥 Referral Task Unlocked!\n\n"
        f"Invite {REQUIRED_REFERRALS} friends using your personal link below.\n\n"
        f"👥 Progress: {referral_count}/{REQUIRED_REFERRALS}\n\n"
        f"🔗 Your Link:\n{referral_link}"
    )


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
