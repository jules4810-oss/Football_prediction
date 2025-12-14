import json
import telebot
import json
import math 
import numpy as np
from scipy.stats import poisson

def load_teams():
    with open("teams.json", "r", encoding="utf-8") as f:
        teams = json.load(f)
    meta = {"version": "1.0"}
    return teams, meta

def predict_match(home, away, teams, meta, max_goals=6):
    if home not in teams or away not in teams:
        return {"error": "Team not found"}

    home_strength = teams[home]
    away_strength = teams[away]

    expected_goals = {
        home: round(home_strength * 1.2, 2),
        away: round(away_strength * 1.0, 2)
    }

    most_likely_score = f"{round(expected_goals[home])}-{round(expected_goals[away])}"

    return {
        "expected_goals": expected_goals,
        "most_likely_score": most_likely_score,
        "outcome_probabilities": {
            "home_win": 0.45,
            "draw": 0.25,
            "away_win": 0.30
        }
    }

# Charger token
with open('config.json', 'r') as f:
    cfg = json.load(f)

TOKEN = cfg.get('8299127138:AAFFnQhFJACOO_vwl0kAaA0uD6MqFpPQgOE', '').strip()
if not TOKEN:
    print("ERROR: TELEGRAM_TOKEN not set in config.json.")
    raise SystemExit(1)

bot = telebot.TeleBot(TOKEN)
teams, meta = load_teams()

# Commande start/help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "Salut! Je suis ton bot de prédiction ⚽\n\n"
        "Commandes:\n"
        "/predict home_team away_team - prédiction d'un match\n"
        "/example - exemple d'utilisation\n"
    )
    bot.reply_to(message, text)

# Exemple
@bot.message_handler(commands=['example'])
def example(message):
    bot.reply_to(message, "Exemple: /predict Paris_SG Real_Madrid")

# Prédiction
@bot.message_handler(commands=['predict'])
def predict_cmd(message):
    args = message.text.split()[1:]
    if len(args) < 2:
        bot.reply_to(message, "Usage: /predict home_team away_team")
        return
    home, away = args[0], args[1]
    result = predict_match(home, away, teams, meta)
    text = (
        f"Match: {home} vs {away}\n"
        f"Expected goals: {result['expected_goals']}\n"
        f"Most likely score: {result['most_likely_score']}\n"
        f"Outcome probabilities: {result['outcome_probabilities']}"
    )
    bot.reply_to(message, text)

# Lancer le bot
if __name__ == '__main__':
    print("Bot Telegram démarré. Polling...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)