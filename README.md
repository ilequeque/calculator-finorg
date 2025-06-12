# 💱 Currency Rate Calculator WebApp

This is a simple and user-friendly **currency rate calculator** built with **Flask (Python)** for the backend and **vanilla JavaScript** for the frontend. It fetches and calculates real-time exchange rates from multiple national banks and displays income and gross profit for agents and providers.

## 🌐 Demo

Coming soon: [https://yourdomain.com](https://yourdomain.com)

---

## 🚀 Features

- 🧮 Calculates income and gross income using commission and markup
- 🌍 Fetches rates from multiple sources:
  - National Bank of Kazakhstan (НБРК)
  - People's Bank of Kazakhstan (Народный Банк)
  - Central Bank of Russia (ЦБРФ)
  - National Bank of the Kyrgyz Republic (Кыргызский НБ)
- 🌐 Supports KZT, USD, RUB, KGS
- 🔄 Real-time rate updates at defined intervals
- 📱 Telegram WebApp integration
- 📊 Localized and user-friendly number formatting

---

## 📸 Screenshots

> _(Optional: Include screenshots or a demo gif here)_

---

## 🛠️ Technologies Used

**Backend:**
- Python 3.x
- Flask
- requests

**Frontend:**
- HTML/CSS (vanilla)
- JavaScript (Telegram WebApp SDK)

**Server:**
- Gunicorn
- Nginx
- Let's Encrypt (HTTPS)

---

## 📦 Setup Instructions

### 🔧 Requirements

- Python 3.8+
- pip
- git
- A Linux VPS (for production deployment)

### 🖥️ Local Development

```bash
git clone https://github.com/yourusername/currency-webapp.git
cd currency-webapp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
