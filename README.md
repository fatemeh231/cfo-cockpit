# 📊 CFO Cockpit — Financial Planning & Forecasting Dashboard

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![Prophet](https://img.shields.io/badge/Prophet-1.1%2B-green.svg)](https://facebook.github.io/prophet/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

> **Interactive revenue forecasting dashboard for 46 major US companies using Prophet AI and SEC EDGAR data.**

---

## 🚀 Live Demo

🔗 **[View the live dashboard](https://gterhgbry2fswa2r6f5rmy.streamlit.app/)

---

## 📖 Overview

This project is a complete **financial planning & forecasting tool** for CFOs and finance teams. It:

- ✅ **Extracts** 26 quarters of real financial data from SEC EDGAR (2.6GB of raw data)
- ✅ **Cleans** and standardizes revenue data for 46 major US companies
- ✅ **Forecasts** revenue 12 quarters ahead using Facebook Prophet (AI)
- ✅ **Visualizes** historical trends and future predictions
- ✅ **Simulates** "what‑if" scenarios (growth rate, marketing spend)
- ✅ **Deploys** as an interactive web app (Streamlit)

---

## 🏢 Companies Included

| Sector | Companies |
|--------|-----------|
| **Technology** | Apple, Microsoft, Google, Amazon, Meta, Nvidia, Tesla, Broadcom, AMD, Oracle, Intel, Cisco, Salesforce, Netflix |
| **Financials** | JPMorgan, Bank of America, Visa, Mastercard, Wells Fargo, Citigroup, Goldman Sachs |
| **Healthcare** | Johnson & Johnson, Eli Lilly, Pfizer, AbbVie, Merck, UnitedHealth |
| **Energy** | Exxon Mobil, Chevron, ConocoPhillips |
| **Retail** | Walmart, Costco, Home Depot, Nike, Starbucks |
| **Communications** | Disney, AT&T, Verizon |
| **Industrials** | GE, Caterpillar, Boeing |
| **Other** | Berkshire Hathaway, Palantir, Uber, Shopify |

**Total: 46 companies | 1,302 revenue records**

---

## 📸 Dashboard Preview

![CFO Cockpit Dashboard](output/dashboard_preview.png)

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
| **Deployment** | Streamlit Cloud / ngrok |

---

## 📁 Project Structure

cfo-cockpit/
│
├── app/
│ └── app.py # Main Streamlit dashboard
│
├── data/
│ └── processed/
│ └── all_companies_revenue.csv # Combined dataset (46 companies)
│
├── src/
│ ├── extract_all_companies.py # Extraction pipeline
│ └── extract_ciks_from_files.py # CIK mapping
│
├── output/ # Screenshots & exports
├── requirements.txt # Python dependencies
└── README.md # This file
text


---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/fatemeh231/cfo-cockpit.git
cd cfo-cockpit

2. Install Dependencies
bash

pip install -r requirements.txt

3. Run the Dashboard Locally
bash

streamlit run app/app.py

🏃 Usage
Run the Dashboard
bash

streamlit run app/app.py

Run the Extraction Pipeline (Optional)

If you want to refresh the data:
bash

python src/extract_all_companies.py

📊 Features
Feature	Description
📈 Historical Revenue	Line chart showing 26 quarters of real data
🔮 AI Forecasting	Prophet predicts 12 quarters ahead with confidence intervals
📊 Company Selector	Dropdown to switch between 46 companies
🧠 Scenario Analysis	Adjust growth rate (%) and marketing spend ($M)
📋 Forecast Table	View exact numbers for future quarters
📱 Responsive	Works on desktop, tablet, and mobile
📌 Key Insights
Metric	Value
Total Companies	46
Total Records	1,302
Date Range	2018 – 2026
Data Source	SEC EDGAR (2.6GB raw data)
Average Accuracy	95%+ confidence intervals
🧠 How the Forecast Works

    Prophet (Facebook/Meta's time-series library) analyzes historical revenue patterns.

    It detects seasonality (quarterly patterns), trends (growth/decline), and holiday effects.

    It generates a forecast with confidence intervals (shaded blue area).

    Users can apply "what-if" scenarios to see how changes affect future revenue.

🚀 Deployment
Streamlit Cloud

📝 Data Sources
Source	Description
SEC EDGAR	Official financial filings for all US public companies
sub.txt	Company metadata (CIK, name, filing type)
num.txt	Financial numbers (revenue, assets, liabilities)
🛡️ License

This project is licensed under the MIT License – see the LICENSE file for details.
🤝 Connect with Me

I'm a Data Engineer & Web Scraping Specialist focused on building end-to-end data pipelines and interactive dashboards.

https://img.shields.io/badge/LinkedIn-Seyedeh%2520Fatemeh%2520Hosseininasab-blue?style=for-the-badge&logo=linkedin
https://img.shields.io/badge/GitHub-fatemeh231-black?style=for-the-badge&logo=github
https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail
📝 Author

Seyedeh Fatemeh Hosseininasab
Data Engineer | Web Scraping Specialist | NLP Enthusiast

Built with ❤️ as a complete brand intelligence and financial forecasting project.
⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!