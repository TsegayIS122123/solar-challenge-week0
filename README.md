# 🌞 Solar Data Discovery - Cross-Country Solar Farm Analysis

[![CI Pipeline](https://github.com/your-username/solar-challenge-week1/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/solar-challenge-week1/actions)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)

A comprehensive data analysis project for MoonLight Energy Solutions to identify high-potential regions for solar installations across Benin, Sierra Leone, and Togo.

## 📋 Project Overview

This project analyzes solar radiation measurement data to support strategic solar investment decisions. As an Analytics Engineer at MoonLight Energy Solutions, the goal is to identify optimal locations for solar farm development that align with the company's sustainability objectives.

### Objective
- **Identify** high-potential regions for solar installation
- **Analyze** environmental factors affecting solar efficiency
- **Provide** data-driven recommendations for strategic investments
- **Compare** solar potential across three West African countries

**Core Areas Covered:**
- Python programming & environment setup  
- Git & GitHub version control  
- CI/CD workflows (GitHub Actions)  
- Data cleaning & exploratory data analysis  
- Statistical comparison between regions  
- Streamlit dashboard development  

## 🧰 Tech Stack

- **Python 3.10+**
- **pandas**, **numpy**, **matplotlib**, **seaborn**, **scipy**
- **Git & GitHub**
- **GitHub Actions** (for CI/CD)
- **Streamlit** (for dashboard visualization)
- **Jupyter Notebooks**


## 🗂️ Dataset Description

The dataset contains solar radiation and environmental measurements with the following key columns:

| Column | Description | Unit |
|--------|-------------|------|
| Timestamp | Date and time of observation | yyyy-mm-dd hh:mm |
| GHI | Global Horizontal Irradiance | W/m² |
| DNI | Direct Normal Irradiance | W/m² |
| DHI | Diffuse Horizontal Irradiance | W/m² |
| Tamb | Ambient Temperature | °C |
| RH | Relative Humidity | % |
| WS | Wind Speed | m/s |
| BP | Barometric Pressure | hPa |
| Cleaning | Cleaning event indicator | 1 or 0 |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- GitHub account

### Installation & Setup

# 1️⃣ Clone the repository

   git clone https://github.com/TsegayIS122123/solar-challenge-week1.git
   cd solar-challenge-week1
# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt   

## 🧾 Final Report
You can read my full project summary and insights here:

📄 [Download the PDF Report](https://drive.google.com/file/d/1kK0khFZT-13XudFeEuPD3aoKQr2bgB2g/view?usp=drive_link)

🖥️ Live Dashboard: [Solar Dashboard](https://tsegayis122123-solar-challenge-week0-appmain-t1wmvd.streamlit.app/)
[Dashboard Screenshot](dashboard_screenshots/)

