import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
FATHER_ID = 264174547
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Оставить заявку", callback_data="application")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚗 Автолизинг\n\n"
        "Хотите узнать условия автолизинга или оставить заявку?\n"
        "Нажмите кнопку ниже, и мы свяжемся с вами.",
        reply_markup=reply_markup,
    )
async def application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    message = (
        "🔔 Новая заявка на автолизинг!\n\n"
        f"Имя: {user.full_name}\n"
        f"Telegram ID: {user.id}\n"
        f"Username: @{user.username if user.username else 'не указан'}\n\n"
        "Этот человек оставил вам заявку."
    )
    try:
        await context.bot.send_message(
            chat_id=FATHER_ID,
            text=message,
        )
        await query.edit_message_text(
            "✅ Ваша заявка отправлена! Мы свяжемся с вами."
        )
    except Exception:
        logging.exception("Не удалось отправить заявку")
        await query.message.reply_text(
            "Не удалось отправить заявку. Попробуйте позже."
        )
def main():
    if not BOT_TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN в настройках Render")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(application, pattern="^application$"))
    app.run_polling()
if __name__ == "__main__":
    main()
