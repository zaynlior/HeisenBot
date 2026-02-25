from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔥 PASTE YOUR NEW BOT TOKEN HERE
BOT_TOKEN = "8726690172:AAHR-uEgB4E8sGkD6YXgUxAGlAa0HNXTptA"

REQUIRED_TAG = "#heisen"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Check if user has #heisen in their name
    full_name = f"{user.first_name or ''} {user.last_name or ''}".lower()

    if REQUIRED_TAG.lower() not in full_name:
        keyboard = [
            [InlineKeyboardButton("Join Channel 1", url="https://t.me/addlist/Hztgg24Yyjc0YmUx")],
            [InlineKeyboardButton("Join Channel 2", url="https://t.me/HeisenOperator")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "⚠️ You must join the following channels to claim rewards:\n\n"
            "#Heisen\n\n"
            "Please join all channels and put #heisen in your name to claim the rewards!.\n\n"
            "After completing, press /start again.",
            reply_markup=reply_markup
        )
        return

    # If name contains #heisen
    await update.message.reply_text(
        "✅ Task Completed!\n\n"
        "🎁 PM @Heisenbergactives for free gift."
    )


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
