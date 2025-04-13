# 🛍️ Vinted Scraper

This project helps you find the best deals on [Vinted.it](https://www.vinted.it/) by automatically searching, saving, and analyzing product listings. It's perfect for reselling or just scoring great finds.

## 🔧 What It Does

- **Scrapes listings** based on your search filters (brand, price, color, etc.)
- **Saves data** into CSV files for each search
- **Analyzes listings** to find:
  - Undervalued items
  - Popular sizes
  - Items with high interest
  - Slow-moving stock
- **Downloads images** of items
- **Filters images** using an AI model to remove incorrect ones
- **Sends WhatsApp alerts** for good deals
- **Handles Vinted chats** (e.g., declines offers, deletes chats)

## 📁 Main Files

- `main.py` – Runs the scraper
- `filters.py` – Sets search filters
- `searches.py` – Your saved searches
- `data analyser.py` – Finds trends and potential deals
- `dataset_cleaner.py` – Removes bad images
- `embedder.py` – AI text classifier for brands or types
- `notifications.py` – Sends WhatsApp messages
- `conversations.py` – Manages your Vinted messages
- `general_functions.py` – Utility helpers (e.g., image downloader)

## ✅ How to Use

1. Set up your searches in `searches.py`
2. Run `main.py`
3. Check your CSV files and image folders
4. Analyze data using `data analyser.py`
5. Get WhatsApp alerts if deals are found
