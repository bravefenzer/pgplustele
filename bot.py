import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    CallbackQueryHandler
)

TOKEN = "7987190781:AAFrVBnjU8O2p-5EyKGbAPhpfcl0aHLQjuY"

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def show_main_menu(update: Update, context: CallbackContext, is_callback=False):
    try:
        # Image URL
        photo_url = "https://i.imghippo.com/files/Cjvd5401gc.jpg"
        
        # Main message text
        message_text = """
🎉 *🎡 LIBRENG SPINS?! Yes! No deposit needed!*

📢 *Appointed by Official PGSoft*
💎 *PAGCOR-Licensed Online Casino*
👉 *Bagong players ng PGPlus makakakuha ng libreng PGSoft Free Spins upon registration! 🆓* 👇

🔗 *Register:* [pgplus.net](https://pgplus.ph/ref/buffguy190)  
📢 *Follow the Telegram group:* [Click Here](https://t.me/pgplusph)  
👍 *Join Facebook Page:* [Click Here](https://www.facebook.com/profile.php?id=61566285694340)
"""

        keyboard = [
            [InlineKeyboardButton("💎Register Here!", web_app=WebAppInfo(url="https://tele-bot-5ie7cf96n-johhny-mongs-projects.vercel.app"))],
            [InlineKeyboardButton("📢Telegram Group", url="https://t.me/pgplusph")],
            [InlineKeyboardButton("👍Facebook Page", url="https://www.facebook.com/profile.php?id=61566285694340")],
            [InlineKeyboardButton("📜 Instructions", callback_data="instruction_command")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)

        if is_callback:
            query = update.callback_query
            await query.answer()
            await query.edit_message_media(
                media=InputMediaPhoto(media=photo_url, caption=message_text, parse_mode="Markdown")
            )
            await query.edit_message_reply_markup(reply_markup=reply_markup)
        else:
            await update.message.reply_photo(
                photo_url,
                caption=message_text,
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            
    except Exception as e:
        logger.error(f"Error showing main menu: {e}")
        try:
            if is_callback:
                await update.callback_query.message.reply_text("⚠️ Failed to load menu. Please try /start")
            else:
                await update.message.reply_text("⚠️ An error occurred. Please try again later.")
        except:
            pass

async def start(update: Update, context: CallbackContext):
    await show_main_menu(update, context, is_callback=False)

async def start_callback(update: Update, context: CallbackContext):
    await show_main_menu(update, context, is_callback=True)

async def instructions_callback(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()
        
        # Instruction image
        photo_url = "https://i.imghippo.com/files/Km5951ibM.jpg"
        
        # Instruction text
        message_text = """
📢 *Step-by-step kung paano sumali:*
💎 *PAGCOR-Licensed Online Casino*
👉 *Mag-register sa* [pgplus.net](https://pgplus.ph/ref/buffguy190) 
👉 *I-claim ang free spins (walang deposit required!)*
👉 *Spin & win! 🤑*
"""

        keyboard = [
            [InlineKeyboardButton("💎Register Here!", web_app=WebAppInfo(url="https://tele-bot-5ie7cf96n-johhny-mongs-projects.vercel.app"))],
            [InlineKeyboardButton("📢Telegram Group", url="https://t.me/pgplusph")],
            [InlineKeyboardButton("👍Facebook Page", url="https://www.facebook.com/profile.php?id=61566285694340")],
            [InlineKeyboardButton("📜 Main Menu", callback_data="start")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Edit the existing message
        await query.edit_message_media(
            media=InputMediaPhoto(media=photo_url, caption=message_text, parse_mode="Markdown")
        )
        await query.edit_message_reply_markup(reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(f"Error in instructions callback: {e}")
        try:
            await query.message.reply_text("⚠️ Failed to show instructions. Please try again.")
        except:
            pass
        
async def help_command(update: Update, context: CallbackContext):
    help_text = """
🤖 *Bot Commands:*
/start - Start the bot and see main options
/help - Show this help message

📌 You can also click the buttons provided for quick access!
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def unknown_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Sorry, I didn't understand that command. Type /help for available commands.")

def main():
    try:
        # Create the Application
        app = ApplicationBuilder().token(TOKEN).build()

        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CallbackQueryHandler(instructions_callback, pattern="^instruction_command$"))
        app.add_handler(CallbackQueryHandler(start_callback, pattern="^start$"))
        app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

        logger.info("✅ Bot is running...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()