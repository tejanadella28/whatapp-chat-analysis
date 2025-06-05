# 📊 WhatsApp Chat Analyzer

<div align="center">
  
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chat-analysis-28.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
  
</div>

![App Screenshot](https://github.com/tejanadella28/whatapp-chat-analysis/blob/main/Screenshot%202025-06-05%20155057.png)

A powerful tool to analyze your WhatsApp chats with beautiful visualizations. Get insights into your messaging patterns, most used words, emojis, and more!

## ✨ Features

- 📈 **Chat Statistics**: Total messages, media shared, links exchanged
- 👥 **User Analysis**: Compare activity between participants in group chats
- 📅 **Timeline Visualizations**: Daily and monthly activity patterns
- ☁️ **Word Cloud**: Visual representation of most frequently used words
- 😂 **Emoji Analysis**: See which emojis dominate your conversations
- 🔗 **Link Extraction**: Discover shared URLs and websites
- 🎨 **Interactive UI**: Clean, user-friendly interface built with Streamlit

## 🚀 Quick Start

1. Export your WhatsApp chat (without media) from:
   - Android: `More options → More → Export chat`
   - iOS: Open chat → Tap contact name → Export Chat

2. Visit the live app: [WhatsApp Chat Analyzer](https://chat-analysis-28.streamlit.app/)

3. Upload your chat file and explore your insights!

## 🛠️ Local Installation

```bash
# Clone the repository
git clone https://github.com/tejanadella28/whatapp-chat-analysis/tree/main
cd whatsapp-chat-analyzer

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
