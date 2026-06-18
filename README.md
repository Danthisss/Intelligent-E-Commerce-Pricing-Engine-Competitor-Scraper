# Intelligent-E-Commerce-Pricing-Engine-Competitor-Scraper

An end-to-end data engineering and business intelligence pipeline designed to automate competitor price monitoring across digital retail platforms. This project automates the extraction of unstructured web data, executes programmatic data cleansing, performs exploratory data analysis (EDA), and deploys a web-based reporting dashboard for strategic decision-making.

---

## Project Overview
In highly competitive e-commerce markets, manual price tracking is inefficient and prone to error. This project provides an automated solution that extracts real-time product metrics (titles, exact pricing, customer ratings, and stock status). By transforming this raw web data into a clean, structured repository, the system generates actionable market insights regarding price distributions, product availability, and vendor margin setups across various categories.

## System Architecture & Workflow

### 1. Data Extraction (Web Scraping)
* Developed a robust modular scraper using `BeautifulSoup4` and `Requests` to parse raw HTML documents from target e-commerce environments.
* Programmed script to navigate multi-page catalogs to systematically compile over 1,000 unique product records while respecting request thresholds.

### 2. Forensic Data Cleansing & Preparation
* Engineered high-efficiency text parsing routines utilizing **Regular Expressions (Regex)** to strip raw formatting, handle symbols, and isolate numerical values.
* Processed and cast raw string metrics into appropriate data types (e.g., transforming text currency like `"£51.77"` into machine-readable floats).
* Handled structural data anomalies, mapped messy text representations of star-ratings into numeric integers, and addressed missing rows using `Pandas` to secure pipeline integrity.

### 3. Exploratory Data Analysis (EDA)
* Applied statistical aggregation to reveal pricing spreads, identifying minimum, maximum, and average retail baseline costs per product category.
* Generated visualizations using `Matplotlib` and `Seaborn` to identify skewness in consumer ratings and expose structural fixed-margin pricing behaviors implemented by online competitors.

### 4. Dashboard Deployment
* Constructed and optimized a dark-theme reporting interface using `Streamlit` to deliver information cleanly to non-technical stakeholders.
* Implemented dynamic multi-variable filtering, real-time data search functionality, and programmatic catalog filters.

---

## 🛠️ Tech Stack & Technical Tools
* **Core Language:** Python
* **Data Engineering & Manipulation:** Pandas, NumPy
* **Web Harvesting Frameworks:** BeautifulSoup4, Requests, Regex (re)
* **Statistical Visualization:** Matplotlib, Seaborn
* **Application Framework & Hosting:** Streamlit

Developed By: Preetham Sharvin Danthi | © 2025 All Rights Reserved
