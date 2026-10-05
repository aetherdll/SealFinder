# 🦭 SealFinder v1.0

SealFinder is a lightweight and interactive Python tool designed to retrieve and analyze metadata (creation date, account age, and region) for TikTok accounts using Snowflake ID parsing.

## 🚀 Features

* **Automatic ID Retrieval:** Automatically fetches the numeric TikTok ID from public profile pages.
* **Snowflake ID Decoding:** Extracts exact creation timestamps mathematically from 64-bit TikTok IDs (`id >> 32`).
* **Precise Account Age Calculation:** Calculates the exact age of the account down to days, months, and years.
* **Clean CLI Interface:** Simple, fast, and user-friendly English terminal interface with DD/MM/YYYY date formatting.

## 📥 Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/SealFinder.git](https://github.com/yourusername/SealFinder.git)
   cd SealFinder

2. Install Depencies:
   ```bash
   pip install -r requirements.txt

## 💻 Usage

   ```bash
   python sf.py

**Enter any TikTok username when prompted, and SealFinder will instantly generate the full analysis report!**

## ⚠️ Disclaimer

**This tool is for educational and informational purposes only. It uses publicly available data and math algorithms.**
