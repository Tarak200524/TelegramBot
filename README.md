# Telegram AI Email Automation Bot

A production-ready Telegram bot that generates professional emails using Mistral AI and sends them via Gmail SMTP.

## Features
- ✨ **AI Powered:** Uses Mistral AI (`mistral-small-2506`) to write professional emails.
- 📧 **Gmail Integration:** Sends emails securely using SMTP SSL.
- 🔄 **Confirmation Workflow:** Shows a draft for user approval before sending.
- 🚀 **Async & Efficient:** Built with `python-telegram-bot` (v20+).

## Project Structure
- `bot.py`: Main bot entry point and Telegram handlers.
- `ai_service.py`: Integration with Mistral AI SDK.
- `email_service.py`: Gmail SMTP logic using `smtplib`.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables (API keys and credentials).

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- A Mistral AI API Key (from [Mistral Console](https://console.mistral.ai/))
- A Gmail Account with **App Password** enabled:
  - Enable 2FA on your Google account.
  - Go to App Passwords and generate one for "Mail".

### 2. Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd telegram-mail-ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your credentials.

### 3. Usage
Run the bot:
```bash
python bot.py
```
Go to your Telegram bot and send a message like:
`recipient@gmail.com | Write an email saying I cannot attend tomorrow meeting`

The bot will generate a draft, show it to you, and wait for your confirmation (SEND/CANCEL).

## Error Handling
The bot handles:
- Invalid message formats.
- Invalid email addresses.
- Mistral AI API errors.
- Gmail SMTP authentication or sending errors.

## Deployment
You can easily deploy this bot on VPS, Heroku, Railway, or Render. Ensure you set the Environment Variables in your hosting provider's dashboard.
