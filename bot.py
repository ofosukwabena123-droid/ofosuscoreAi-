import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_ID = os.getenv("ADMIN_USER_ID", "")

free_picks = "No free predictions published yet."
premium_picks = "No premium predictions published yet."


def is_admin(update):
    return (
        ADMIN_ID
        and str(update.effective_user.id) == ADMIN_ID
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ WELCOME TO OFOSU SCORE AI!\n\n"
        "Daily Football Predictions\n\n"
        "/free - Free predictions\n"
        "/premium - Private premium predictions\n"
        "/myid - Get your Telegram ID\n"
        "/help - Help\n\n"
        "Correct scores and 2+ odds predictions.\n"
        "Predictions are not guaranteed."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "OFOSU SCORE AI BOT\n\n"
        "/free - View free picks\n"
        "/premium - View premium picks\n"
        "/myid - Your Telegram ID\n\n"
        "Admin commands:\n"
        "/postfree - Publish free picks\n"
        "/postpremium - Publish premium picks"
    )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your Telegram ID: {update.effective_user.id}"
    )


async def free_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(free_picks)


async def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text(
            "🔒 Premium predictions are private."
        )
        return

    await update.message.reply_text(premium_picks)


async def postfree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global free_picks

    if not is_admin(update):
        await update.message.reply_text("Admin only.")
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Usage:\n/postfree Match | Score | Odds"
        )
        return

    free_picks = "⚽ FREE PREDICTIONS\n\n" + text

    await update.message.reply_text(
        "✅ Free prediction published!"
    )


async def postpremium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global premium_picks

    if not is_admin(update):
        await update.message.reply_text("Admin only.")
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            "Usage:\n/postpremium Match | Score | Odds"
        )
        return

    premium_picks = "🔒 PRIVATE PREMIUM PICKS\n\n" + text

    await update.message.reply_text(
        "✅ Premium prediction saved!"
    )


def main():
    if not TOKEN:
        raise RuntimeError("Telegram token is missing.")

    if not ADMIN_ID:
        raise RuntimeError("Admin ID is missing.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("free", free_command))
    app.add_handler(CommandHandler("premium", premium_command))
    app.add_handler(CommandHandler("postfree", postfree))
    app.add_handler(CommandHandler("postpremium", postpremium))

    print("OFOSU SCORE AI is running!")

    app.run_polling()


if __name__ == "__main__":
    main()
