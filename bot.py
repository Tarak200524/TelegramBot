import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
from ai_service import AIService
from email_service import EmailService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime) - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize services
ai_service = AIService()
email_service = EmailService()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the command /start is issued."""
    welcome_text = (
        "👋 Welcome to the AI Email Automation Bot!\n\n"
        "To send an email, use the following format:\n"
        "`recipient@example.com | Your instruction for the email` \n\n"
        "Example:\n"
        "`boss@company.com | Write a polite email asking for a meeting tomorrow.`"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the user's message, generates a draft, and asks for confirmation."""
    text = update.message.text
    
    if "|" not in text:
        await update.message.reply_text(
            "❌ Invalid format. Please use: `recipient@email.com | instruction`",
            parse_mode='Markdown'
        )
        return

    try:
        recipient, instruction = map(str.strip, text.split("|", 1))
        
        # Simple email validation
        if "@" not in recipient or "." not in recipient:
            await update.message.reply_text("❌ Please provide a valid email address.")
            return

        status_message = await update.message.reply_text("🤖 Generating draft...")

        # Generate email draft using Mistral AI
        draft = await ai_service.generate_email(instruction)
        
        # Store draft and recipient in user_data
        context.user_data['pending_email'] = {
            'recipient': recipient,
            'draft': draft
        }

        keyboard = [
            [
                InlineKeyboardButton("SEND ✅", callback_data='send_email'),
                InlineKeyboardButton("CANCEL ❌", callback_data='cancel_email')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        preview_text = (
            f"📧 *Draft Preview*\n\n"
            f"*To:* {recipient}\n\n"
            f"*Content:*\n{draft}\n\n"
            f"Should I send this email?"
        )
        
        await status_message.delete()
        await update.message.reply_text(preview_text, reply_markup=reply_markup, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text(f"⚠️ An error occurred: {str(e)}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the SEND and CANCEL button clicks."""
    query = update.callback_query
    await query.answer()

    action = query.data
    pending = context.user_data.get('pending_email')

    if not pending:
        await query.edit_message_text("❌ No pending email found.")
        return

    if action == 'send_email':
        await query.edit_message_text("📤 Sending email...")
        try:
            # Assuming the first line of the draft might be a subject or we use a generic one
            # For simplicity, we'll use a generic subject or try to extract it
            subject = "Automated AI Assistant Email"
            
            email_service.send_email(
                recipient=pending['recipient'],
                subject=subject,
                body=pending['draft']
            )
            
            success_text = (
                f"✅ *Email Sent Successfully!*\n\n"
                f"*Recipient:* {pending['recipient']}\n\n"
                f"*Sent Content:*\n{pending['draft']}"
            )
            await query.edit_message_text(success_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Email sending error: {e}")
            await query.edit_message_text(f"❌ Failed to send email: {str(e)}")
            
    elif action == 'cancel_email':
        await query.edit_message_text("🗑️ Email draft cancelled.")

    # Clear pending email data
    context.user_data['pending_email'] = None

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Error: TELEGRAM_TOKEN not found in environment.")
    else:
        application = ApplicationBuilder().token(token).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        application.add_handler(CallbackQueryHandler(button_callback))
        
        print("Bot is running...")
        application.run_polling()
