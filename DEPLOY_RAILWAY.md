Railway deployment instructions for this Telegram echo bot

1) Prepare repo
   - Make sure the repo has these files at project root: `bot.py`, `config.py`, `requirements.txt`, `Procfile`.
   - `config.py` is already set to read the bot token from the environment variable `TOKEN`.

2) Connect to Railway
   - Create a new project on Railway and connect your GitHub repository (or push this repo to GitHub and connect it).
   - Choose to deploy from the repository's main branch.

3) Set environment variables (important)
   - In the Railway project settings, add an environment variable named `TOKEN` and paste your bot token there.
   - Optionally set `DB_NAME` if you want a different name for the users file (default: `users.json`).

4) Start command / Procfile
   - The repo contains a `Procfile` with `web: python bot.py`. Railway will use that to run the bot as a long-lived process.
   - Long-polling bots work as a persistent process on Railway. If you prefer, you can mark the service as a worker instead.

5) Persistent storage note
   - `users.json` is used as a simple file DB. Railway ephemeral filesystems may be reset between deploys. For production use consider a proper DB (Postgres, Redis, etc.).

6) Local testing
   - Create a local `.env` file or set the environment variable in your shell: `export TOKEN=your_token_here`
   - Install deps and run:

```bash
pip install -r requirements.txt
python bot.py
```

7) Security
   - Do NOT commit your bot token to the repo. Keep it in Railway secrets or local `.env` only.

If you want, I can also add a small `README.md` section or create a `docker` setup for Railway. Tell me which you prefer next.