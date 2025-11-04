# Deploying Telegram Bot to Render.com

## Prerequisites
- A GitHub account
- Your Telegram bot token from @BotFather
- A Render.com account

## Deployment Steps

1. **Prepare Your Repository**
   - Push your code to GitHub if you haven't already
   - Make sure you have these files in your repository:
     - `bot.py` (main bot code)
     - `config.py` (configuration)
     - `requirements.txt` (dependencies)

2. **Set Up on Render.com**
   - Log in to [Render](https://dashboard.render.com/)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - Name: `your-bot-name`
     - Runtime: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python bot.py`
     - Plan: Choose "Free"

3. **Configure Environment Variables**
   - In your Render dashboard, go to the "Environment" section
   - Add the following environment variable:
     - Key: `TOKEN`
     - Value: Your Telegram bot token
   - (Optional) Add `DB_NAME` if you want to customize the database filename

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your bot
   - Check the logs to make sure everything is working

## Local Testing
Before deploying, test locally:

```bash
# Create a .env file (don't commit this!)
echo "TOKEN=your_bot_token_here" > .env

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

## Important Notes
- Never commit your bot token to the repository
- The free tier on Render should work fine for most bot use cases
- If your bot stops responding, check the Render dashboard logs
- Render's free tier may sleep after inactivity, which is normal