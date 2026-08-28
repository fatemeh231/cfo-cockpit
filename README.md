# 📊 CFO Cockpit — Financial Planning & Forecasting

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![Prophet](https://img.shields.io/badge/Prophet-1.1%2B-green.svg)](https://facebook.github.io/prophet/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

> **Interactive revenue forecasting dashboard for 46 major US companies using Prophet AI and real SEC EDGAR data.**

---

## 🌐 Live Demo

🔗 **[View the live dashboard here!](https://gterhgbry2fswa2r6f5rmy.streamlit.app/)**

*(Click the link above to see the live app in action — no installation required!)*

---

## 📖 Overview

This project is a complete **financial planning & forecasting tool** for CFOs and finance teams. It:

- ✅ **Extracts** 26 quarters of real financial data from SEC EDGAR (2.6GB of raw data)
- ✅ **Cleans** and standardizes revenue data for **46 major US companies**
- ✅ **Forecasts** revenue 12 quarters ahead using **Facebook Prophet (AI)**
- ✅ **Visualizes** historical trends and future predictions
- ✅ **Simulates** "what‑if" scenarios (growth rate, marketing spend)
- ✅ **Deploys** as an interactive web app (Streamlit)

---

## 🏢 Companies Included

| Sector | Companies |
|--------|-----------|
| **Technology** | AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA, AVGO, AMD, ORCL, INTC, CSCO, CRM, NFLX |
| **Financials** | JPM, BAC, V, MA, WFC, C, GS |
| **Healthcare** | JNJ, LLY, PFE, ABBV, MRK, UNH |
| **Energy** | XOM, CVX, COP |
| **Retail** | WMT, COST, HD, NKE, SBUX |
| **Communications** | DIS, T, VZ |
| **Industrials** | GE, CAT, BA |
| **Other** | BRK.B, PLTR, UBER, SHOP |

**Total: 46 companies | 1,302 revenue records**

---

##



*Interactive dashboard showing revenue trends, AI forecasts, and scenario analysis.*

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Data Extraction** | Python, Pandas, SEC EDGAR (sub.txt, num.txt) |
| **Data Cleaning** | Pandas, NumPy |
| **Forecasting** | Facebook Prophet (time-series AI) |
| **Visualization** | Plotly, Matplotlib |
| **Dashboard** | Streamlit |
| **Deployment** | Streamlit Cloud |

---

## 📁 Project Structure

```
cfo-cockpit/
│
├── app/
│   └── app.py                    # Main Streamlit dashboard
│
├── data/
│   └── processed/
│       └── all_companies_revenue.csv    # Combined dataset (46 companies)
│
├── src/
│   ├── extract_all_companies.py  # Extraction pipeline
│   └── extract_ciks_from_files.py # CIK mapping
│
├── output/                       # Screenshots & exports
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/fatemeh231/cfo-cockpit.git
cd cfo-cockpit
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard Locally

```bash
streamlit run app/app.py
```

---

## 🏃 Usage

### Run the Dashboard

```bash
streamlit run app/app.py
```

### Run the Extraction Pipeline (Optional)

If you want to refresh the data:

```bash
python src/extract_all_companies.py
```

---

## 📊 Features

| Feature | Description |
|---------|-------------|
| 📈 **Historical Revenue** | Line chart showing 26 quarters of real data |
| 🔮 **AI Forecasting** | Prophet predicts 12 quarters ahead with confidence intervals |
| 📊 **Company Selector** | Dropdown to switch between 46 companies |
| 🧠 **Scenario Analysis** | Adjust growth rate (%) and marketing spend ($M) |
| 📋 **Forecast Table** | View exact numbers for future quarters |
| 📱 **Responsive** | Works on desktop, tablet, and mobile |

---

## 🧠 How the Forecast Works

1. **Prophet** (Facebook/Meta's time-series library) analyzes historical revenue patterns.
2. It detects **seasonality** (quarterly patterns), **trends** (growth/decline), and **holiday effects**.
3. It generates a forecast with **confidence intervals** (shaded blue area).
4. Users can apply **"what-if" scenarios** to see how changes affect future revenue.

---

## 📌 Key Insights

| Metric | Value |
|--------|-------|
| **Total Companies** | 46 |
| **Total Records** | 1,302 |
| **Date Range** | 2018 – 2026 |
| **Data Source** | SEC EDGAR (2.6GB raw data) |
| **Average Accuracy** | 95%+ confidence intervals |

---

## 🛡️ License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🤝 Connect with Me

I'm a **Data Engineer & Web Scraping Specialist** focused on building end-to-end data pipelines and interactive dashboards.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Seyedeh%20Fatemeh%20Hosseininasab-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/seyedeh-fatemeh-hosseininasab-7320bb322/)
[![GitHub](https://img.shields.io/badge/GitHub-fatemeh231-black?style=for-the-badge&logo=github)](https://github.com/fatemeh231)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:seyedehfatemehhosseininasab2@gmail.com)

---

## 📝 Author

**Seyedeh Fatemeh Hosseininasab**  
*Data Engineer | Web Scraping Specialist | NLP Enthusiast*

Built with ❤️ as a complete financial forecasting and brand intelligence project.

---

### ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---
```

---

