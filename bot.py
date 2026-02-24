from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔥 PASTE YOUR NEW TOKEN BELOW
BOT_TOKEN = "8726690172:AAHR-uEgB4E8sGkD6YXgUxAGlAa0HNXTptA"

CHANNELS = [ "@HeisenOperator"]
REQUIRED_TAG = "#heisen"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Check channel membership
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user.id)
            if member.status not in ["member", "administrator", "creator"]:
                await update.message.reply_text(
                    "⚠️ You must join the following channels to claim rewards:\n\n"
                    "#Heisen\n"
                    "@HeisenOperator\n\n"
                    "Please join all channels and put #heisen in your name to claim the rewards!.\n\n"
                    "After joining, press /start again."
                )
                return
        except:
            await update.message.reply_text("Make sure the bot is admin in all channels.")
            return

    # Check name tag
    full_name = f"{user.first_name or ''} {user.last_name or ''}".lower()

    if REQUIRED_TAG.lower() not in full_name:
        await update.message.reply_text(
            "⚠️ You must put #heisen in your name to claim the reward.\n\n"
            "Update your Telegram name and press /start again."
        )
        return

    await update.message.reply_text(
        "✅ Task Completed!\n\n"
        "🎁 PM @HeisenbergActive free gift."
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
