# Discord Bot GPT

## Features
- [x] Memory
- [x] Token usage calculator
- [x] Custom trigger
- [ ] Memory keep alive through builds/deployment
- [ ] Web surfing

## Usage

### Commands
- `!chat` is the trigger command. You can change it by changing the value of `TRIGGER` variable in `main.py`.
- `!chat total_tokens` to print total tokens used with amount spent in RM. You can change it by changing the value of `TOTAL_TOKENS_TRIGGER` variable in `main.py`.

### Local development
- Create `.env` file with `DISCORD_KEY` variable(your discord bot token) and `OPENAI_KEY` variable(your openai api key).

## Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/wIUjNC?referralCode=E44ptv)