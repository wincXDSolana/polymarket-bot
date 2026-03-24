# polymarket-bot
🚀 MoonDev-inspired Python Polymarket bot for 5-min BTC/ETH/SOL Up/Down markets | Mean Reversion + MACD signals | Gasless limit orders | Run 24/7 on Railway or VPS

# Polymarket Mean Reversion Bot 🚀

**A simple, beginner-friendly Python bot for trading 5-minute Up/Down crypto markets on Polymarket**  
Inspired by MoonDev’s YouTube tutorials (Claude + Polymarket = Free Money?, Mean Reversion Trading Bot, and 5-min live coding sessions).

### What it does
- Scans active **5-minute BTC, ETH, SOL Up-or-Down markets** in real time  
- Uses **mean-reversion logic** (price deviation from recent average) + **MACD filter** to find high-probability entries  
- Places **gasless limit orders** automatically (no fees, just like MoonDev shows)  
- Avoids duplicate positions and includes basic risk guards  
- Runs 24/7 while you sleep — perfect for small-size incubation ($5–$20 per trade)

**Why mean reversion?**  
MoonDev’s backtests show that retail gets chopped on these short-term markets. When price deviates too far, it tends to snap back. This bot bets against the extremes with MACD confirmation — exactly the edge he teaches in his public videos.

### Features
- ✅ Fully gasless via official `py-clob-client` SDK  
- ✅ Real-time market scanner using Polymarket Gamma API  
- ✅ Simple MACD + deviation signals (easy to tweak with Claude/Grok)  
- ✅ Built-in position checker & logging  
- ✅ Dry-run mode for safe testing  
- ✅ Deployable on Railway, Replit, VPS, or even iPad + Termius
