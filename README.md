# 🏠 FamilySpend - Family Expense Tracker

A beautiful, production-ready family expense tracker with mobile-first design, supporting 5 user profiles, 25+ expense categories, interactive dashboards, **credit card management**, and bilingual support (English/Telugu).

![FamilySpend](https://img.shields.io/badge/Version-1.1-purple) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![Flask](https://img.shields.io/badge/Flask-3.0+-red) ![UI](https://img.shields.io/badge/Design-Glassmorphism-blue)

## ✨ New in v1.1: Credit Card Power-Up!
- **💳 Credit Card Management**: Track multiple credit cards, spending limits, and billing cycles.
- **🎨 Modern UI/UX**: Stunning glassmorphism design, vibrant gradients, and smooth micro-animations.
- **📱 Smart Dashboard**: Track credit utilization and available balance in real-time.
- **💸 Linked Expenses**: Associate expenses directly with specific credit cards.

## 🚀 Key Features

### 📊 **Core Functionality**
- **5 User Profiles**: Person1-4 and Common profile.
- **25+ Categories**: From Groceries to Electronics, fully categorized.
- **Interactive Dashboards**: Visual charts for trends and breakdowns.
- **Credit Card Tracker**: Manage cards, check utilization, and track billing cycles.
- **Smart Filters & Export**: Analyze data and download CSV reports.

### 🎨 **Design & UX**
- **Mobile-First**: Optimized touch targets and responsive layout.
- **Glassmorphism**: Modern, translucent card designs.
- **Visual Feedback**: Interactive hover states and ripple effects.
- **Dark/Light Theme**: Eye-friendly themes.
- **Swipe Gestures**: Easy management on mobile.

### 🌐 **Multilingual**
- **English/Telugu Support**: Instant toggle between languages.
- **Localized Categories**: All items translated.

### 💾 **Tech Stack**
- **Backend**: Python Flask + SQLite (No setup required!)
- **Frontend**: HTML5, CSS3 (Variables + Flexbox/Grid), Vanilla JS.
- **Charts**: Chart.js for beautiful visualizations.

## 🚀 Quick Start & Deployment

### Local Run
1. **Install**: `pip install flask flask-cors`
2. **Run**: `python app.py`
3. **Open**: `http://localhost:5000`

### 📱 Mobile Access
Access from your phone on the same WiFi!
1. Find your PC's IP (e.g., `192.168.1.39`).
2. Open `http://YOUR_IP:5000` on your phone.

### ☁️ Cloud Deployment
Deploy for free on **PythonAnywhere** or **Render** to access 24/7.
- Includes `requirements.txt` and `.gitignore` for easy deployment.
- See `cloud_deployment_guide.md` in the repo for step-by-step instructions.

## 📖 Usage Guide
1. **Add Cards**: Go to "Cards" tab -> Add your credit cards.
2. **Add Expenses**: Tap "Add" -> Select Profile & Category -> Optionally link a Credit Card.
3. **Analyze**: Check Dashboard for spending trends and Card tab for credit utilization.

## 📂 Project Structure
```
familys_spend/
├── app.py              # Flask backend
├── index.html          # Main UI
├── style.css           # Modern CSS styles
├── script.js           # Logic & Charts
├── data.db             # Local database
├── requirements.txt    # Cloud dependencies
└── README.md           # This file
```

---
**Made with ❤️ for smart families.**
*Version 1.1 | January 2026*
